import torch
from torch.utils.data.dataset import IterableDataset
from torch.utils.data import Dataset, DataLoader
import numpy as np


class DQNDataset(IterableDataset):
    def __init__(self, replay_memory, batch_size):
        self.replay_memory = replay_memory
        self.batch_size = batch_size

    def __iter__(self):
        states, actions, amounts, dones, next_states, rewards = self.replay_memory.sample(self.batch_size)
        for i in range(len(dones)):
            yield states[i], actions[i], amounts[i], dones[i], next_states[i], rewards[i]

class TestDataset(Dataset):
    # test data는 test_values.shape = (500, 245, 5) -> 500개의 종목, 245일, 5개의 feature로 구성
    def __init__(self, data, window_size):
        self.data = data
        self.WINDOW_SIZE = window_size
        
    def __len__(self):
        return self.data.shape[1] - self.WINDOW_SIZE + 1 # 245일 중 window_size만큼 뺀 값이 반환
        
    def __getitem__(self, idx):
        return self.data[:, idx:idx+self.WINDOW_SIZE, :] # 245일 중 1일씩 이동하면서 window_size만큼 데이터를 반환 (sliding window)
    