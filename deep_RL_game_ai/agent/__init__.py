from utils.constant import PlayerAction


class Agent(object):
    """The basic agent class for the game of gathering and wolfpack"""
    def __init__(self):
        self.action = None
        self.player_idx = None
        self.is_prey = False

    def begin_episode(self):
        """Start a new episode"""
        # raise NotImplementedError
        self.action = PlayerAction.STAND_STILL
        # self.player = player

    def act(self, observation):
        """ Called at each loop iteration to choose and execute an action.

        Returns:
            None
        """
        raise NotImplementedError

from .human import HumanAgent
from .random_agent import RandomAgent
