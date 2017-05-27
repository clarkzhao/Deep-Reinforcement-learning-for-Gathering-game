from gui.gathering import *
from gui.wolfpack import *

from agent.human import *
from agent.random_agent import *
from agent.prey_agent import *

if __name__ == '__main__':
    Game = GatheringGUI()
    # Game = WolfpackGUI()
    Game.set_up()
    # If you want to try random agent
    # agent_list = [HumanAgent(), RandomAgent(), PreyAgent()]
    agent_list = [HumanAgent(), RandomAgent()]
    Game.load_agent(agent_list)
    Game.run_episode()
