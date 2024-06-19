from envs.trading import StockTradingEnv
from collections import namedtuple, deque
from utils.training_utils import ReplayMemory,sector_load_data
from models.models.dqn import DQN
from models.litmodels.litmodeldqn import LitModelDQN
from itertools import count
from glob import glob
from tqdm import tqdm
from lightning.pytorch import Trainer
from pytorch_lightning.callbacks import Callback

import logging
import math
import random
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import pandas as pd
import numpy as np

from utils.setup_utils import (
    get_configs,
    init_configs,
    init_settings,
)
from utils.training_utils import Transition, ReplayMemory, sector_load_data

""" Config Setting """

args = get_configs()
args = init_configs(args)
init_settings(args)
args.DATA_DIR = f'{args.BASE_DATA_DIR}/refined_data/{args.NATION}/{args.MARKET}/*.csv'
args.SECTOR_DIR = f'{args.BASE_DATA_DIR}/{args.NATION}/{args.MARKET}/modified_{args.MARKET}_top500_sector_mcap.csv'

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(message)s', 
                    filename='training_68.log', 
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def load_sector_train_env():
    data_dir = args.DATA_DIR
    sector_dir = args.SECTOR_DIR
    train_items, train_values, test_items, test_values, sectors = sector_load_data(data_dir, sector_dir)
    args.episode_length = train_items.shape[1]
    train_env = StockTradingEnv(data=train_values, initial_investment=args.bugget, args=args, sector_indices=sectors)
    return train_env

def main():
    train_env = load_sector_train_env()

    num_episodes = args.num_episodes
    batch_size = args.BATCH_SIZE
    window_size = args.WINDOW_SIZE
    n_step = args.episode_length
    # n_step - window_size + 1 에서 미지수 x를 곱한 값이 10000과 가장 가까운 값을 찾고 이것을 replay_memory의 크기로 설정
    x = int(10000 / (n_step - window_size + 1))
    args.SIZE_OF_REPLAYMEMORY = x * (n_step - window_size + 1)
    replay_memory_size = args.SIZE_OF_REPLAYMEMORY
    args.WARM_START_STEPS = replay_memory_size
    warm_start_steps = args.WARM_START_STEPS
    steps_per_epoch = math.ceil(n_step / batch_size)
    steps_per_episode = n_step - window_size + 1
    num_epochs = math.ceil(num_episodes * steps_per_episode / steps_per_epoch)
        
    logging.info(f"Number of episodes: {num_episodes}")
    logging.info(f"Batch size: {batch_size}")
    logging.info(f"Window size: {window_size}")
    logging.info(f"Data Length: {n_step}")
    logging.info(f"Replay memory size: {replay_memory_size}")
    logging.info(f"Warm start steps: {warm_start_steps}")
    logging.info(f"Number of steps per epoch: {steps_per_epoch}")
    logging.info(f"Number of steps per episode: {steps_per_episode}")
    logging.info(f"Number of Max epochs: {num_epochs}")

    ''' Train model ''' 
    model = LitModelDQN(env=train_env, model=DQN, args=args)
    model.populate()
    devices = list(map(int, args.GPU_NUM.split(",")))
    trainer = Trainer(
        accelerator='gpu',
        devices=devices,
        max_epochs=num_epochs,
        check_val_every_n_epoch=1, # 매 에폭마다 체크포인트 저장
        log_every_n_steps=1,  # 매 스텝마다 로그 기록
    )
    trainer.fit(model)
    
if __name__ == "__main__":
    import traceback
    try:
        main()
    except Exception as e:
        print(f"Error:\n\n{e}")
        print(f"Traceback:\n\n{traceback.format_exc()}")