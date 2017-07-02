from utils.constant import *

import sys
import pygame
import matplotlib.pyplot as plt
import numpy as np
from game.gathering import *
import json
import pygame
import os
from utils.constant import *

class CliGame(object):

    def __init__(self):
        self.fps_clock = None
        self.env = None
        self.agent_list = []
        self.timestep_watch = Stopwatch()
        self.logger = Params().logger

    def set_up(self):
        self.logger.warning("Command line environment setting up")
        with open('gathering.json') as cfg:
            env_config = json.load(cfg)
        self.env = EnvironmentGathering(env_config)

    def load_agent(self, agent_list: list):
        """ Load the RL agent into the Game GUI. """
        self.agent_list = agent_list.copy()
        idx = 0
        for agent in self.agent_list:
            agent.player_idx = idx
            idx += 1

    def show(self, img):
        plt.imshow(img, interpolation='nearest')
        plt.draw()
        # plt.show()

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

        # Determine who is agent and who is opponent?
        self.env.player_list[0].is_agent = True
        # A flag for whether the agent is controlled by human
        # timestep_delay = GameSetting.HUMAN_TIMESTEP_DELAY if is_human else GameSetting.AI_TIMESTEP_DELAY
        timestep_delay = GameSetting.HUMAN_TIMESTEP_DELAY

        # Main game loop.
        running = True
        while running:
            for agent in self.agent_list:
                agent.action = PlayerAction.STAND_STILL
            # Update game state.
            timestep_timed_out = self.timestep_watch.time() >= timestep_delay

            # Update the environment for all players' action
            if timestep_timed_out:
                self.timestep_watch.reset()
                for agent in self.agent_list:
                    agent.action = agent.act(self.env.player_list[agent.player_idx].observation)
                    self.env.take_action(agent.action, self.env.player_list[agent.player_idx])
                    self.env.move(self.env.player_list[agent.player_idx])
            player = self.env.player_list[1]
            img = player.convert_observation_to_rgb()
            self.show(img)
            self.env.grid.clear_beam_area()
            self.env.update_front_of_players()
            self.fps_clock.tick(GameSetting.FPS_LIMIT)

