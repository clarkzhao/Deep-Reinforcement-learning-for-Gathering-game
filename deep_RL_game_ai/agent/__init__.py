from utils.constant import PlayerAction
import numpy as np
from utils.constant import *

class Agent(object):
    """The basic agent class for the game of gathering and wolfpack"""
    def __init__(self):
        self.player_idx = None
        self.is_prey = False
        self.is_human = False
        self.is_DQN = False
        self.step = None  # total number of steps in all training episode
        self.action = None  # current action
        self.total_reward = None  # total reward in an episode
        self.n_actions = len(ALL_PLAYER_ACTIONS)  # total number of actions

        # log agent information
        self.action_stats = np.zeros(self.n_actions)  # actions information in an episode
        self.position_stats = None


    def begin_episode(self):
        """Start a new episode"""
        # raise NotImplementedError
        self.action = PlayerAction.STAND_STILL
        self.total_reward = 0
        self.action_stats = np.zeros(self.n_actions)
        # self.player = player

    def act(self, observation):
        """ Called at each loop iteration to choose and execute an action.

        Returns:
            None
        """
        raise NotImplementedError

    def display_action_stats(self):
        info = "\n"
        for action, value in enumerate(self.action_stats):
            info += PlayerAction.toString(action) + ': ' + str(value) + '\n'
        return info

from .basic import HumanAgent
from .basic import RandomAgent
from .basic import PreyAgent
