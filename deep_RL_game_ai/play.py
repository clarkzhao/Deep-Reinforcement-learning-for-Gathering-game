from gui.gui import *
from agent.basic import *
from game.cli import CliGame
from utils.constant import *
from agent.dqn import *
from game.trainer import *
if __name__ == '__main__':
    # Game = WolfpackGUI()
    # Game = CliGame()
    Game = AgentTrainer()
    Game.set_up()
    # If you want to try random agent
    # agent_list = [HumanAgent(), RandomAgent(), PreyAgent()]
    agent_list = [DQNAgent(), DQNAgent()]
    Game.load_agent(agent_list)
    Game.fit_model()

    # Game = GatheringGUI()
    # Game.set_up()
    # agent_list = [HumanAgent(), RandomAgent()]
    # Game.load_agent(agent_list)
    # Game.run_episode()
