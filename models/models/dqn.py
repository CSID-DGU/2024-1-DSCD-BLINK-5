import torch
import torch.nn as nn


class DQN(nn.Module):
    def __init__(self, state: int, n_actions: int):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state, 128)
        self.fc2 = nn.Linear(128, 128)
        self.action_head = nn.Linear(128, n_actions * 3)
        self.num_head = nn.Linear(n_actions * 3 + 128, n_actions)

    def forward(self, x):
        if x.dim() == 3:
            x = x.unsqueeze(0)

        b, _, _, _ = x.shape

        h = x.reshape(b, -1)
        h = torch.relu(self.fc1(h))
        h = torch.relu(self.fc2(h))
        action = self.action_head(h)

        num = self.num_head(torch.cat((action, h), 1))
        
        # Ensure no negative amounts in the output
        num = torch.relu(num)

        return action, num
    
