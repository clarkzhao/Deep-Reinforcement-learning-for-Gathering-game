from agent import Agent
from utils.constant import ALL_PLAYER_ACTIONS
from utils.constant import PlayerAction
import random


class RandomAgent(Agent):
    """
        The agent that takes random action 
        uniformly over all possible actions
    """

    def __init__(self):
        super(RandomAgent, self).__init__()
        self.is_human = False
        pass

    def begin_episode(self):
        super(RandomAgent, self).begin_episode()
        pass

    def act(self, observation):
        return random.choice(ALL_PLAYER_ACTIONS)
        # return PlayerAction.STAND_STILL

    def __str__(self):
        return "random agent"