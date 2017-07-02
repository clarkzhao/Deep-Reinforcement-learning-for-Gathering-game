from utils.constant import *
from game.wolfpack import *
from game.gathering import *
import sys
import pygame
import matplotlib.pyplot as plt
import numpy as np
import json

class GUIBase(object):

    def __init__(self):
        pygame.init()
        self.screen = None
        self.fps_clock = None
        self.env = None
        self.agent_list = []
        self.timestep_watch = Stopwatch()

    def set_up(self):
        pass

    def load_agent(self, agent_list: list):
        """ Load the RL agent into the Game GUI. """
        self.agent_list = agent_list.copy()
        idx = 0
        for agent in self.agent_list:
            agent.player_idx = idx
            idx += 1

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

    def draw_a_cell(self, x, y):
        """ Draw the cell specified by the field coordinates. """
        cell_coords = pygame.Rect(
            x * GameSetting.CELL_SIZE,
            y * GameSetting.CELL_SIZE,
            GameSetting.CELL_SIZE,
            GameSetting.CELL_SIZE,
        )
        if self.env.view_array[y,x] == CellType.EMPTY:
            pygame.draw.rect(self.screen, Colors.SCREEN_BACKGROUND, cell_coords)
        else:
            color = Colors.CELL_TYPE[self.env.view_array[y, x]]
            pygame.draw.rect(self.screen, color, cell_coords)

    def draw_all_cells(self):
        """ Draw the entire game frame. """
        for x in range(self.env.grid.width):
            for y in range(self.env.grid.height):
                self.draw_a_cell(x, y)

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

    def show(self, img):
        plt.ion()
        plt.imshow(img, interpolation='nearest')
        plt.show()

    def run_episode(self):
        """ Run the GUI player for a single episode. """
        self.fps_clock = pygame.time.Clock()

        # Initialize the environment.
        self.timestep_watch.reset()
        self.env.new_episode()

        for agent in self.agent_list:
            agent.begin_episode()
            if agent.is_prey:
                self.env.player_list[agent.player_idx].is_prey = True

        # A flag for whether the agent is controlled by human
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

            # If human made a move just update the environment for this action
            if human_made_move:
                for agent in self.agent_list:
                    if agent.is_human:
                        self.env.take_action(agent.action, self.env.player_list[agent.player_idx])
                        self.env.move(self.env.player_list[agent.player_idx])
                        # self.env.get_observation()
                        # img = self.env.player_list[agent.player_idx].convert_observation_to_rgb()
                        # self.show(img)

            # Update the environment for all players' action
            if timestep_timed_out:
                self.timestep_watch.reset()
                for agent in self.agent_list:
                    if not agent.is_human:
                        agent.action = agent.act(self.env.player_list[agent.player_idx].observation)
                        self.env.take_action(agent.action, self.env.player_list[agent.player_idx])
                        self.env.move(self.env.player_list[agent.player_idx])
                        self.env.get_observation()

            for agent in self.agent_list:
                if agent.is_human:
                    img = self.env.player_list[agent.player_idx].convert_observation_to_rgb()
                    self.show(img)
                    self.env.convert_view(self.env.player_list[agent.player_idx])


            # Draw all cells
            if GameSetting.GUI:
                self.draw_all_cells()
                pygame.display.update()
            self.env.grid.clear_beam_area()
            self.env.update_front_of_players()
            self.fps_clock.tick(GameSetting.FPS_LIMIT)

class GatheringGUI(GUIBase):

    def __init__(self):
        super(GatheringGUI, self).__init__()


    def set_up(self):
        with open('gathering.json') as cfg:
            env_config = json.load(cfg)
        self.env = EnvironmentGathering(env_config)
        screen_size = (self.env.grid.width * GameSetting.CELL_SIZE, self.env.grid.height * GameSetting.CELL_SIZE)
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill(Colors.SCREEN_BACKGROUND)
        pygame.display.set_caption('Gathering')

class WolfpackGUI(GUIBase):

    def __init__(self):
        super(WolfpackGUI, self).__init__()

    def set_up(self):
        with open('wolfpack.json') as cfg:
            env_config = json.load(cfg)
        self.env = EnvironmentWolfpack(env_config)
        screen_size = (self.env.grid.width * GameSetting.CELL_SIZE, self.env.grid.height * GameSetting.CELL_SIZE)
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill(Colors.SCREEN_BACKGROUND)
        pygame.display.set_caption('Wolfpack')