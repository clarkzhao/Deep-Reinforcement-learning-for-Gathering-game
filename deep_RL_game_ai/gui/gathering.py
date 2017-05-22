from game.environment import *
from utils.constant import *
from agent import HumanAgent
from agent.random_agent import RandomAgent

import sys
import json
import pygame


class GatheringGUI():

    def __init__(self):
        pygame.init()
        self.screen = None
        self.fps_clock = None
        self.env = None
        # self.agent = HumanAgent()
        self.agent_list = []
        self.timestep_watch = Stopwatch()

    def set_up(self):
        with open('10x10-blank.json') as cfg:
            env_config = json.load(cfg)
        self.env = Environment(env_config)
        screen_size = (self.env.grid.width * GameSetting.CELL_SIZE, self.env.grid.height * GameSetting.CELL_SIZE)
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill(Colors.SCREEN_BACKGROUND)
        pygame.display.set_caption('Gathering')

    def load_agent(self, agent1, agent2):
        """ Load the RL agent into the Game GUI. """
        self.agent_list.append(agent1)
        self.agent_list.append(agent2)

    def draw_one_cell(self, x, y):
        """ Draw the cell specified by the field coordinates. """
        cell_coords = pygame.Rect(
            x * GameSetting.CELL_SIZE,
            y * GameSetting.CELL_SIZE,
            GameSetting.CELL_SIZE,
            GameSetting.CELL_SIZE,
        )
        if self.env.grid[x, y] == CellType.EMPTY:
            pygame.draw.rect(self.screen, Colors.SCREEN_BACKGROUND, cell_coords)
        else:
            color = Colors.CELL_TYPE[self.env.grid[x, y]]
            pygame.draw.rect(self.screen, color, cell_coords)

    def draw_all_cells(self):
        """ Draw the entire game frame. """
        for x in range(self.env.grid.width):
            for y in range(self.env.grid.height):
                self.draw_one_cell(x, y)

    def run_episode(self):
        """ Run the GUI player for a single episode. """
        self.fps_clock = pygame.time.Clock()

        # Initialize the environment.
        self.timestep_watch.reset()
        self.env.new_episode()

        for agent in self.agent_list:
            agent.begin_episode()

        # A flag for whether the agent is controlled by human
        # is_human = isinstance(self.agent, HumanAgent)
        # timestep_delay = GameSetting.HUMAN_TIMESTEP_DELAY if is_human else GameSetting.AI_TIMESTEP_DELAY
        timestep_delay = GameSetting.HUMAN_TIMESTEP_DELAY

        # Main game loop.
        running = True
        while running:
            for agent in self.agent_list:
                agent.action = PlayerAction.STAND_STILL

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in GAME_CONTROL_KEYS:
                        for agent in self.agent_list:
                            if agent.is_human:
                                agent.action = self.map_key_to_action(event.key)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update game state.
            timestep_timed_out = self.timestep_watch.time() >= timestep_delay

            # If human made any move make the environment update
            human_made_move = False
            for agent in self.agent_list:
                if agent.is_human:
                    if agent.action != PlayerAction.STAND_STILL:
                        human_made_move = True
                    else:
                        human_made_move = False

            if timestep_timed_out or human_made_move:
                self.timestep_watch.reset()
                i = 0
                for agent in self.agent_list:
                    if not agent.is_human:
                        agent.action = agent.act()
                    self.env.take_action(agent.action, self.env.player_list[i])
                    self.env.move(self.env.player_list[i])
                    i += 1

            # Draw all cells
            self.draw_all_cells()
            self.env.grid.clear_beam_area()
            pygame.display.update()
            self.fps_clock.tick(GameSetting.FPS_LIMIT)

    def map_key_to_action(self, key):
        """ Convert a keystroke to an environment action. """
        actions = [
            PlayerAction.STEP_FORWARD,
            PlayerAction.STEP_LEFT,
            PlayerAction.STEP_BACKWARD,
            PlayerAction.STEP_RIGHT,
            PlayerAction.ROTATE_COUNTERCLOCKWISE,
            PlayerAction.ROTATE_CLOCKWISE,
            PlayerAction.USE_BEAM,
            PlayerAction.STAND_STILL
        ]
        key_idx = GAME_CONTROL_KEYS.index(key)
        return actions[key_idx]

if __name__ == '__main__':
    gatheringGame = GatheringGUI()
    gatheringGame.set_up()
    # If you want to try random agent
    gatheringGame.load_agent(HumanAgent(), RandomAgent())
    gatheringGame.run_episode()
