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
        self.agent = HumanAgent()
        self.timestep_watch = Stopwatch()

    def set_up(self):
        with open('10x10-blank.json') as cfg:
            env_config = json.load(cfg)
        self.env = Environment(env_config)
        screen_size = (self.env.grid.width * GameSetting.CELL_SIZE, self.env.grid.height * GameSetting.CELL_SIZE)
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill(Colors.SCREEN_BACKGROUND)
        pygame.display.set_caption('Gathering')

    def load_agent(self, agent):
        """ Load the RL agent into the Game GUI. """
        self.agent = agent

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
        self.agent.begin_episode()


        # A flag for whether the agent is controlled by human
        is_human = isinstance(self.agent, HumanAgent)
        timestep_delay = GameSetting.HUMAN_TIMESTEP_DELAY if is_human else GameSetting.AI_TIMESTEP_DELAY

        # Main game loop.
        running = True
        while running:
            action = PlayerAction.STAND_STILL

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if is_human and event.key in GAME_CONTROL_KEYS:
                        action = self.map_key_to_action(event.key)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update game state.
            timestep_timed_out = self.timestep_watch.time() >= timestep_delay
            human_made_move = is_human and action != PlayerAction.STAND_STILL

            if timestep_timed_out or human_made_move:
                self.timestep_watch.reset()

                if not is_human:
                    action = self.agent.act()

                self.env.choose_action(action)
                self.env.move()

            # Draw all cells
            self.draw_all_cells()
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
    # gatheringGame.load_agent(RandomAgent())
    gatheringGame.run_episode()
