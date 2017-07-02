from utils.constant import *

import sys
import pygame
import matplotlib.pyplot as plt
import numpy as np
from game.gathering import *
import json
import pygame
import time
import os
from utils.constant import *

class AgentTrainer(object):

    def __init__(self):
        self.fps_clock = None
        self.screen = None
        self.visual = DQNSetting.VISUAL
        self.env = None
        self.agent_list = []
        self.timestep_watch = Stopwatch()
        self.logger = Params().logger

        # episodes and steps in each episode
        self.step = None
        self.step_in_an_episode = None
        self.n_episode_steps = DQNSetting.TOTAL_STEPS_PER_EPISODE
        self.n_episodes = DQNSetting.TOTAL_NUM_EPISODE

        self.training = None
        self.start_time = None


    def set_up(self):
        self.logger.warning("Command line environment setting up")
        with open('gathering.json') as cfg:
            env_config = json.load(cfg)
        self.env = EnvironmentGathering(env_config)
        self.logger.warning("Loading map successfully")
        self.start_time = time.time()
        if self.visual:
            pygame.init()
            screen_size = (self.env.grid.width * GameSetting.CELL_SIZE, self.env.grid.height * GameSetting.CELL_SIZE)
            self.screen = pygame.display.set_mode(screen_size)
            self.screen.fill(Colors.SCREEN_BACKGROUND)
            pygame.display.set_caption('Gathering')


    def load_agent(self, agent_list):
        """ Load the RL agent into the Game GUI. """
        self.agent_list = agent_list.copy()
        idx = 0
        for agent in self.agent_list:
            agent.player_idx = idx
            idx += 1

    def new_episode(self):
        self.env.new_episode()
        self.step_in_an_episode = 0
        for agent in self.agent_list:
            agent.begin_episode()
            if agent.is_prey:
                self.env.player_list[agent.player_idx].is_prey = True
            if agent.is_DQN:
                self.logger.warning("agent: {} in control of player {}".format(agent.player_idx,
                                    self.env.player_list[agent.player_idx].idx))

    def run_episode(self):
        """ Run the GUI player for a single episode. """
        self.fps_clock = pygame.time.Clock()

        # Initialize the environment.
        self.new_episode()

        # A flag for whether the agent is controlled by human
        # timestep_delay = GameSetting.HUMAN_TIMESTEP_DELAY if is_human else GameSetting.AI_TIMESTEP_DELAY
        timestep_delay = GameSetting.AI_TIMESTEP_DELAY

        # Main game loop.
        running = True
        step_in_an_episode = 0
        while step_in_an_episode < DQNSetting.EPISODE_LENGTH and running:
            for agent in self.agent_list:
                agent.action = PlayerAction.STAND_STILL
            # Update game state.
            timestep_timed_out = self.timestep_watch.time() >= timestep_delay

            # Update the environment for all players' action
            if timestep_timed_out:
                self.timestep_watch.reset()
                # Log of overall information
                if self.step_in_an_episode % DQNSetting.LOG_FRE == 0:
                    self.logger.warning("Reporting       @ Step: " + str(self.step_in_an_episode) +
                                        " | Elapsed Time: " + str(time.time() - self.start_time))
                for agent in self.agent_list:
                    agent.step = self.step_in_an_episode
                    observation = self.env.player_list[agent.player_idx].convert_observation_to_rgb()
                    agent.action = agent.act(observation)
                    self.env.take_action(agent.action, self.env.player_list[agent.player_idx])
                    self.env.move(self.env.player_list[agent.player_idx])
                    cur_reward = self.env.player_list[agent.player_idx].reward
                    agent.total_reward += cur_reward
                    if agent.is_DQN and cur_reward != 0:
                        print(cur_reward)
                    if agent.is_DQN:
                        agent.optimizer = agent.optim(agent.q_network.parameters(), lr=agent.lr)
                        agent.learn(cur_reward, False)
                        # Log of DQN training information
                        if self.step_in_an_episode % DQNSetting.LOG_FRE == 0:
                            self.logger.warning("Agent     ID: {}".format(agent.player_idx))
                            self.logger.warning("Training Stats:   epsilon:          {}".format(agent.eps))
                            self.logger.warning("Training Stats:   total_reward:     {}".format(agent.total_reward))
                            self.logger.warning("Training Stats:   avg_reward:       {}".format(
                                agent.total_reward / self.step_in_an_episode if self.step_in_an_episode > 0 else 0.))
                self.step_in_an_episode += 1

                if self.visual:
                    self.draw_all_cells()
                    pygame.display.update()
                self.env.grid.clear_beam_area()
                self.env.update_front_of_players()
            self.fps_clock.tick(GameSetting.FPS_LIMIT)

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