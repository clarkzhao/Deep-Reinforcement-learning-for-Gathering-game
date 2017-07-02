from agent import Agent
from utils.constant import PlayerAction

from utils.constant import ALL_PREY_ACTIONS
from utils.constant import ALL_PLAYER_ACTIONS
import random


class HumanAgent(Agent):
    """The agent controller by human"""

    def __init__(self):
        super(HumanAgent, self).__init__()
        self.is_human = True
        pass

    def begin_episode(self):
        super(HumanAgent, self).begin_episode()
        pass

    def act(self, observation):
        return PlayerAction.STAND_STILL

    def __str__(self):
        return "human agent"

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

class PreyAgent(Agent):
    """
        The agent that takes random action
        uniformly over all possible actions
    """

    def __init__(self):
        super(PreyAgent, self).__init__()
        self.is_human = False
        self.is_prey = True

    def begin_episode(self):
        super(PreyAgent, self).begin_episode()

    def act(self, observation):
        return random.choice(ALL_PREY_ACTIONS)
        # return PlayerAction.STAND_STILL

    def __str__(self):
        return "prey agent"