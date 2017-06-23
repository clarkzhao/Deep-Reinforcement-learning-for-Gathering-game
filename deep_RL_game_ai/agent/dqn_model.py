import torch.nn as nn
import torch.nn.functional as F
import random
from collections import namedtuple


class DQN(nn.Module):
    def __init__(self, in_features=4, num_actions=18):
        """
        A deep Q-network described in
        https://storage.googleapis.com/deepmind-media/papers/multi-agent-rl-in-ssd.pdf
        :param in_features: number of features of input
        :param num_actions: total number of all possible actions in the game gathering and wolfpack
        """
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(in_features, 32)
        self.fc2 = nn.Linear(32, 32)
        self.fc3 = nn.Linear(32, num_actions)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)