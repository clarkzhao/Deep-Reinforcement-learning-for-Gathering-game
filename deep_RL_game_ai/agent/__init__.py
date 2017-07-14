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
        self.is_DRUQN = False
        self.step = None  # total number of steps in all training episode
        self.step_in_an_episode = None  # number of steps in an episode
        self.action = None  # current action
        self.total_reward = None  # total reward accumulated in a single episode
        self.n_actions = len(ALL_PLAYER_ACTIONS)  # total number of actions

        # log agent information
        self.action_stats = np.zeros(self.n_actions, dtype='int8')  # actions information in an episode
        self.position_stats = np.zeros((13, 33), dtype='int')


    def begin_episode(self):
        """Start a new episode"""
        self.action = PlayerAction.STAND_STILL
        self.total_reward = 0
        self.action_stats = np.zeros(self.n_actions)
        self.position_stats = np.zeros((13, 33), dtype='int8')
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
            info += PlayerAction.to_string(action) + ': ' + str(value) + '\n'
        return info

    def display_position_stats(self):
        info = '\n'.join(
            ' '.join(str(j) for j in i)
            for i in self.position_stats)
        return info

from .basic import HumanAgent
from .basic import RandomAgent
from .basic import PreyAgent
