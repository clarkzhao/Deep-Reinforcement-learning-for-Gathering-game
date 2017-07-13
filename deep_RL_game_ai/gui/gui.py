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
            if agent.is_DQN:
                agent.step = 0
                agent.training = False
                if agent.load_model(os.getcwd()+"/output/saved_models/"+"2017-07-12_13-03-45_id-1_episode-448.pth"):
                    print("Loading DQN successfully")

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

    def map_key_to_action(self, player_id, key):
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
        if player_id == 0:
            key_idx = GAME_CONTROL_KEYS.index(key)
        else:
            key_idx = GAME_CONTROL_KEYS_2.index(key)
        return actions[key_idx]

    def show(self, img):
        plt.ion()
        plt.clf()
        plt.imshow(img, interpolation='nearest')
        plt.draw()

    def show_position(self, position_stats):
        plt.ion()
        plt.imshow(position_stats, cmap='hot', interpolation='nearest')
        plt.draw()

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

            # Update for human's action
            human_made_move = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in GAME_CONTROL_KEYS:
                        human_made_move = True
                        for agent in self.agent_list:
                            if agent.is_human and agent.player_idx == 0:
                                agent.action = self.map_key_to_action(0, event.key)
                    if event.key in GAME_CONTROL_KEYS_2:
                        human_made_move = True
                        for agent in self.agent_list:
                            if agent.is_human and agent.player_idx == 1:
                                agent.action = self.map_key_to_action(1, event.key)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update for AI's action
            if self.timestep_watch.time() >= timestep_delay:
                self.timestep_watch.reset()
                for agent in self.agent_list:
                    if not agent.is_human:
                        agent.step += 1
                        observation = self.env.player_list[agent.player_idx].convert_observation_to_rgb()
                        agent.action = agent.act(observation)

            # for agent in self.agent_list:
            agent = self.agent_list[0]
            self.env.take_action(agent.action, self.env.player_list[agent.player_idx])

            # Update the environment
            self.env.move()
            agent = self.agent_list[1]
            self.env.take_action(agent.action, self.env.player_list[agent.player_idx])
            self.env.move()
            for agent in self.agent_list:
                if agent.is_human:
                    reward = self.env.player_list[agent.player_idx].reward
                    agent.total_reward += reward
                    # img = self.env.player_list[agent.player_idx].convert_observation_to_rgb()
                    # self.show(img)
                    self.env.convert_view(self.env.player_list[agent.player_idx])
                    if reward != 0:
                        print(agent.player_idx, reward)
                        print("total reward: {}".format(agent.total_reward))

            # if human_made_move:
            #     img = self.env.player_list[0].convert_observation_to_rgb()
            #     self.show(img)

            # Draw all cells
            if GameSetting.GUI:
                self.draw_all_cells()
                pygame.display.update()
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