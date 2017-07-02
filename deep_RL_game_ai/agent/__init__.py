from utils.constant import PlayerAction


class Agent(object):
    """The basic agent class for the game of gathering and wolfpack"""
    def __init__(self):
        self.player_idx = None
        self.is_prey = False
        self.is_human = False
        self.is_DQN = False
        # number of steps in an episode
        self.step = None
        self.action = None
        self.total_reward = None

    def begin_episode(self):
        """Start a new episode"""
        # raise NotImplementedError
        self.action = PlayerAction.STAND_STILL
        self.total_reward = 0
        self.step = 0
        # self.player = player

    def act(self, observation):
        """ Called at each loop iteration to choose and execute an action.

        Returns:
            None
        """
        raise NotImplementedError

from .basic import HumanAgent
from .basic import RandomAgent
from .basic import PreyAgent
