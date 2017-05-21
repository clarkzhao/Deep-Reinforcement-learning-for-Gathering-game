from agent import Agent
from utils.constant import ALL_PLAYER_ACTIONS
import random


class RandomAgent(Agent):
    """
        The agent that takes random action 
        uniformly over all possible actions
    """

    def __init__(self):
        pass

    def begin_episode(self):
        pass

    def act(self):
        return random.choice(ALL_PLAYER_ACTIONS)
