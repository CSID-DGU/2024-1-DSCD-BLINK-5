from lightning import LightningModule
from easydict import EasyDict
from random import random
from utils.training_utils import ReplayMemory, torch2np
from torch.utils.data import DataLoader
from datasets.dqn import DQNDataset
import math
import torch
import torch.nn as nn
import numpy as np
from copy import deepcopy
import logging
import torch.nn.functional as F

from utils.setup_utils import (
    get_configs,
)
args = get_configs()
args.DATA_DIR = f'{args.BASE_DATA_DIR}/{args.NATION}/{args.MARKET}/*.csv'
args.SECTOR_DIR = f'{args.BASE_DATA_DIR}/{args.NATION}/{args.MARKET}/modified_{args.MARKET}_top500_sector_mcap.csv'


class DQNAgent:
    def __init__(self, env, replay_memory, args):
        self.env = env
        self.replay_memory = replay_memory
        self.args = args
        self.sector_indices = self.env.sector_indices # 추가
        self.reset()
        self.state = self.env.reset()
        
    def reset(self):
        self.state = self.env.reset()
    
    def softmax_allocation(self, amounts, cash_available, prices, sector_indices):
        unique_sectors = np.unique(sector_indices)
        sector_allocation = np.zeros(len(np.unique(self.env.sector_indices)))

        sector_amounts = []
        for sector in unique_sectors:
            sector_mask = (sector_indices == sector)
            sector_amounts.append(amounts[sector_mask].sum())
        sector_prob = F.softmax(torch.tensor(sector_amounts))
            
        buy_amounts = np.zeros_like(prices)
        for idx, sector in enumerate(unique_sectors):
            sector_mask = (sector_indices == sector)
            if np.any(prices > 0):
                individual_amounts = F.softmax(torch.tensor(amounts[sector_mask]), dim=0)
                sector_individual_amounts = individual_amounts * sector_prob[idx]
                scaled_amount = (sector_individual_amounts / sector_individual_amounts.sum()) * cash_available
                buy_amounts[sector_mask] = np.floor(scaled_amount.cpu().numpy() / prices[sector_mask]).astype(int)

        return buy_amounts
    
    def select_action(self, policy_net, epsilon):
        sample = np.random.random()

        if sample > epsilon:
            with torch.no_grad():
                state = torch.tensor(self.state['state'], dtype=torch.float32, device=self.args.device)
                action, amount = policy_net(state)
                action = action.reshape(-1, 3).argmax(1)
                action = torch2np(action).squeeze()
                amount = torch2np(amount).squeeze()
                
                current_prices = self.env.stock_price[:, -1]  # 가장 최근 가격 선택
                sector_indices = self.env.sector_indices  # 섹터 인덱스 정보 사용
                
                buy_mask = (action == 2)
                sell_mask = (action == 0)
                stay_mask = (action == 1)
                
                if any(action == 2):  # 매수 행동이 있을 경우만 처리
                    buy_mask = (action == 2)
                    buy_amounts = self.softmax_allocation(amount[buy_mask], self.env.cash_in_hand, current_prices[buy_mask], sector_indices[buy_mask])
                    current_buy_price = np.sum(buy_amounts * current_prices[buy_mask])
                    current_sell_price = np.sum(amount[sell_mask] * current_prices[sell_mask])
                    if current_buy_price > self.env.cash_in_hand + current_sell_price:
                        high_ratio = math.ceil(current_buy_price / (self.env.cash_in_hand + 1e-9))
                        if high_ratio != 0:
                            buy_amounts = buy_amounts // high_ratio
                    amount[buy_mask] = buy_amounts
                    
                if any(action == 0):  # 매도 행동이 있을 경우만 처리
                    sell_mask = (action == 0)
                    owned_stocks = self.env.stock_owned[sell_mask]
                    amount[sell_mask] = np.minimum(amount[sell_mask], owned_stocks)
                    
                if any(action == 1):
                    stay_mask = (action == 1)
                    amount[stay_mask] = 0
        else:
            action, amount = self.env.sample()
            
        return action, amount
        
    @torch.no_grad()
    def play_step(self, policy_net, epsilon):
        action, amount = self.select_action(policy_net, epsilon)
        next_state, reward, done, _ = self.env.step(action, amount)
        self.replay_memory.push(self.state, action, amount, done, next_state, reward)
        self.state = next_state

        if done:
            self.reset()

        return reward, done
        
    
class LitModelDQN(LightningModule):
    def __init__(self, env, model: nn.Module, args: EasyDict):
        super().__init__()
        
        self.env = env
        self.args = args
        self.__init_model(model)
            
        self.memory = ReplayMemory(capacity=args.SIZE_OF_REPLAYMEMORY)
        self.agent = DQNAgent(env, self.memory, args)
        
        self.total_reward = 0
        self.episode_reward = 0
        
    def __init_model(self, model):
        self.policy_net = model(self.args.n_actions * self.args.WINDOW_SIZE * self.args.n_features, self.args.n_actions)
        self.target_net = model(self.args.n_actions * self.args.WINDOW_SIZE * self.args.n_features, self.args.n_actions)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        
    def populate(self):
        for _ in range(self.args.WARM_START_STEPS):
            self.agent.play_step(self.policy_net, 1.0)
            logging.info(f"Populate: replay_memory_size={len(self.memory)}")

    def forward(self, x):
        return self.policy_net(x)
    
    def criterion(self, batch):
        state, action, amount, done, next_state, reward = batch

        state_action_values, state_amount_values = self.policy_net(state['state'])
        state_action_values = state_action_values.gather(1, action)
        state_action_amount_values = state_action_values * state_amount_values
        
        with torch.no_grad():
            b, _, _, _ = next_state['state'].shape
            next_state_action_values, next_state_amount_values = self.target_net(next_state['state'])
            next_state_action_values = next_state_action_values.reshape(b, self.args.n_actions, 3).max(2).values
            next_state_action_values[done] = 0.0
            next_state_action_amount_values = next_state_action_values * next_state_amount_values
        
        expected_state_action_values= (
            next_state_action_values * self.args.GAMMA
        ) + reward.unsqueeze(1)
        
        expected_state_amount_values = (
            next_state_amount_values * self.args.GAMMA
        ) + reward.unsqueeze(1)
        
        expected_state_action_amount_values = (
            next_state_action_amount_values * self.args.GAMMA
        ) + reward.unsqueeze(1)


        criterion = nn.SmoothL1Loss()
        
        # 1. return criterion(state_action_amount_values, expected_state_action_amount_values)
        # 2. return criterion(state_action_values, expected_state_action_values) # action만 고려한 경우
        # 3. return criterion(state_amount_values, expected_state_amount_values) # amount만 고려한 경우
        # 4. return criterion(state_action_values, expected_state_action_values) + criterion(state_amount_values, expected_state_amount_values) # 2 + 3
        return criterion(state_action_amount_values, expected_state_action_amount_values) + criterion(state_action_values, expected_state_action_values) + criterion(state_amount_values, expected_state_amount_values) # 1 + 2 + 3
        # 1~5 중 가장 좋은 loss 기반으로 6번.
        
        
    def get_epsilone(self, steps_done):
        eps_threshold = self.args.EPS_END + (self.args.EPS_START - self.args.EPS_END) * math.exp(
            -1.0 * steps_done / self.args.EPS_DECAY
        )
        return eps_threshold
    
    def training_step(self, batch, batch_idx):
        epsilon = self.get_epsilone(self.global_step)
        reward, done = self.agent.play_step(self.policy_net, epsilon)
        self.episode_reward += reward
        loss = self.criterion(batch)
        self.log("replay_memory_size", len(self.memory), prog_bar=True)

        if done:
            self.total_reward = self.episode_reward
            self.episode_reward = 0
            
        if self.global_step % 10 == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())
        
        # # soft-update mechanism
        # target_net_state_dict = self.target_net.state_dict()
        # policy_net_state_dict = self.policy_net.state_dict()
        # for key in policy_net_state_dict:
        #     target_net_state_dict[key] = (
        #         self.args.TAU * policy_net_state_dict[key]
        #         + (1 - self.args.TAU) * target_net_state_dict[key]
        #     )
        # self.target_net.load_state_dict(target_net_state_dict)
        
        logging.info(f"epoch={self.current_epoch}, steps={self.global_step}, current_step={self.env.current_step}, loss={loss}, episode_reward={self.episode_reward}, total_reward={self.total_reward}, epsilon={epsilon}, done={done}")
        self.log("episode_reward", self.episode_reward, prog_bar=True)
        self.log("total_reward", self.total_reward, prog_bar=True)
        self.log("epsilon", epsilon, prog_bar=True)
        self.log("loss", loss, prog_bar=True)
        self.log("current_step", self.env.current_step, prog_bar=True)
        self.log("done", done, prog_bar=True)
        return loss 
    
    def configure_optimizers(self):
        self.optimizer = torch.optim.AdamW(self.policy_net.parameters(), lr=self.args.LR, amsgrad=True)
        return self.optimizer

    def __dataloader__train(self):
        dataset = DQNDataset(self.memory, self.args.episode_length)
        dataloader = DataLoader(
            dataset=dataset,
            batch_size=self.args.BATCH_SIZE,
        )
        return dataloader

    def train_dataloader(self):
        return self.__dataloader__train() 