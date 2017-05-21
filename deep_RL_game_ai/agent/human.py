from agent import Agent
from utils.constant import PlayerAction


class HumanAgent(Agent):
    """The agent controller by human"""

    def __init__(self):
        pass

    def begin_episode(self):
        pass

    def act(self):
        return PlayerAction.STAND_STILL
