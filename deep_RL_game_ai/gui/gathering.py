from game.environment import *
from utils.constant import *
import sys
import json
import pygame


class GatheringGUI():
    GAME_CONTROL_KEYS = [
        pygame.K_UP,
        pygame.K_LEFT,
        pygame.K_DOWN,
        pygame.K_RIGHT,
        pygame.K_q,
        pygame.K_e,
        pygame.K_SPACE,
        pygame.K_z
    ]

    def __init__(self):
        pygame.init()
        self.screen = None
        self.fps_clock = None
        self.env = None
        self.timestep_watch = Stopwatch()

    def set_up(self):
        with open('10x10-blank.json') as cfg:
            env_config = json.load(cfg)
        self.env = Environment(env_config)
        screen_size = (self.env.grid.width * GameSetting.CELL_SIZE, self.env.grid.height * GameSetting.CELL_SIZE)
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill(Colors.SCREEN_BACKGROUND)
        pygame.display.set_caption('Gathering')

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

        timestep_delay = GameSetting.HUMAN_TIMESTEP_DELAY
        # Main game loop.
        running = True
        while running:
            action = PlayerAction.STAND_STILL

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in self.GAME_CONTROL_KEYS:
                        action = self.map_key_to_action(event.key)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update game state.
            timestep_timed_out = self.timestep_watch.time() >= timestep_delay
            self.env.choose_action(action)
            self.env.move()
            # next_position, next_direction = self.env.choose_action(action)
            # self.env.timestep(next_position, next_direction)

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
        key_idx = self.GAME_CONTROL_KEYS.index(key)
        return actions[key_idx]

if __name__ == '__main__':
    gatheringGame = GatheringGUI()
    gatheringGame.set_up()
    gatheringGame.run_episode()
