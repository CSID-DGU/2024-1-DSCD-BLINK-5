from collections import namedtuple, deque
from glob import glob
from tqdm import tqdm
import numpy as np
import pandas as pd
import random

Transition = namedtuple(
    "Transition", ("state", "action", "amount", "done", "next_state", "reward")
)


class ReplayMemory:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.memory = deque(maxlen=capacity)
        
    def __len__(self):
        return len(self.memory)

    def push(self, *args):
        # if memory is full, remove the oldest element
        if len(self.memory) >= self.capacity:
            self.memory.popleft()
            
        self.memory.append(Transition(*args))

    def sample(self, batch_size: int):
        indices = np.random.choice(len(self.memory), batch_size, replace=False)
        states, actions, amounts, dones, next_states, rewards = zip(
            *[self.memory[idx] for idx in indices]
        )
        
        return (
            np.array(states),
            np.array(actions),
            np.array(amounts),
            np.array(dones, dtype=bool),
            np.array(next_states),
            np.array(rewards, dtype=np.float32),
        )

def load_data(data_path, split_date="2022-12-31"):
    item_list = sorted(glob(data_path))
    train_items = []
    test_items = []
    for idx, item_dir in enumerate(tqdm(item_list)):
        item = pd.read_csv(item_dir)
        train_item = item[item['Date'] <= split_date]
        test_item = item[item['Date'] > split_date]
        train_items.append(train_item.values)
        test_items.append(test_item.values)

    train_items = np.array(train_items)
    test_items = np.array(test_items)
    train_values = train_items[:, :, 1:].astype(np.float32)
    test_values = test_items[:, :, 1:].astype(np.float32)
    
    return train_items, train_values, test_items, test_values

def load_train_test_data(data_path):
    train_items, train_values, test_items, test_values = load_data(data_path, "2022-12-31")
    return train_items, train_values, test_items, test_values

def sector_load_data(data_path, sector_path, split_date='2022-12-31'):
    item_list = sorted(glob(data_path))
    sector_df = pd.read_csv(sector_path)
    # 한국 데이터일 때 (아래) - sector_df의 종목코드를 6자리로 만들고 부족한 만큼 맨 앞에 0을 채움
    # sector_df['종목코드'] = sector_df['종목코드'].apply(lambda x: str(x).zfill(6))
    train_items = []
    test_items = []
    sectors = []
    
    sector_mapping = dict(zip(sector_df['종목코드'], sector_df['섹터']))
    
    for idx, item_dir in enumerate(tqdm(item_list)):
        item = pd.read_csv(item_dir)
        item['Sector'] = sector_mapping[item_dir.split('/')[-1].rsplit('.', 1)[0]]
        # 한국 데이터일 때 (아래)
        #item['Sector'] = sector_mapping[item_dir.split('/')[-1].split('.')[0]]
        train_item = item[item['Date'] <= split_date]
        test_item = item[item['Date'] > split_date]
        
        # sector to index
        unique_sectors = sector_df['섹터'].unique()
        sector_to_index = {sector: idx for idx, sector in enumerate(unique_sectors)}
        train_item['Sector'] = train_item['Sector'].map(sector_to_index)
        test_item['Sector'] = test_item['Sector'].map(sector_to_index)
        train_items.append(train_item.values)
        test_items.append(test_item.values)
        sectors.append(train_item['Sector'].values[0])
        
    train_items = np.array(train_items)
    test_items = np.array(test_items)
    sectors = np.array(sectors)
    
    train_date_list = train_items[0, :, 0]
    train_values = train_items[:, :, 1:6].astype(np.float32)
    train_sectors = train_items[:, 0, 6]
    
    test_date_list = test_items[0, :, 0]
    test_values = test_items[:, :, 1:6].astype(np.float32)
    test_sectors = test_items[:, 0, 6]
    
    return train_items, train_values, test_items, test_values, sectors


def torch2np(x_torch):
    x_np = x_torch.detach().cpu().numpy()
    return x_np
