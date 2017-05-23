from utils.constant import PlayerAction


class Agent(object):
    """The basic agent class for the game of gathering and wolfpack"""
    def __init__(self):
        self.action = None
        self.player_idx = None

    def begin_episode(self):
        """Start a new episode"""
        # raise NotImplementedError
        self.action = PlayerAction.STAND_STILL
        # self.player = player

    def act(self):
        """ Called at each loop iteration to choose and execute an action.

        Returns:
            None
        """
        # raise NotImplementedError
        pass

from .human import HumanAgent
from .random_agent import RandomAgent
