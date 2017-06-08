from agent import Agent
from utils.constant import ALL_PREY_ACTIONS
from utils.constant import PlayerAction
import random


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
