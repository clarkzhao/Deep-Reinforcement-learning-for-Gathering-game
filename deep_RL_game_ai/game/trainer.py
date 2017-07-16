from utils.constant import *
import sys
import pygame
import matplotlib.pyplot as plt
import numpy as np
from game.gathering import *
import json
import time
from utils.constant import *
import torch
import pickle
from agent.model import *


class AgentTrainer(object):

    def __init__(self):
        self.fps_clock = None
        self.screen = None
        self.visual = DQNSetting.VISUAL_GUI
        self.env = None
        self.agent_list = []
        self.timestep_watch = Stopwatch()
        self.logger = Params().logger

        # episodes and steps in each episode
        self.step_in_an_episode = None
        self.n_steps = DQNSetting.TOTAL_STEPS_PER_EPISODE
        self.n_episodes = DQNSetting.TOTAL_NUM_EPISODE
        self.step = None  # total number of steps for training
        self.episode = None  # number of episode for training
        self.eval_episode = None  # number of episode for evaluation
        self.eval_steps = DQNSetting.EVAL_STEPS
        self.evaluation = None
        self.start_time = None
        self.visualize = DQNSetting.VISUAL_DATA

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
        self.step = 0
        self.episode = 0

    def load_agent(self, agent_list):
        """ Load the RL agent into the Game GUI. """
        self.agent_list = agent_list.copy()
        idx = 0
        for agent in self.agent_list:
            agent.player_idx = idx
            idx += 1
            if agent.is_DQN:
                agent.optimizer = agent.optim(agent.q_network.parameters(), lr=agent.lr, alpha=0.95, eps=0.01)

    def load_model(self):
        if self.agent_list[0].load_model(DQNSetting.PRETRAINED_MODEL_1):
            self.logger.warning("Loading model 1 successfully")
        if self.agent_list[1].load_model(DQNSetting.PRETRAINED_MODEL_2):
            self.logger.warning("Loading model 2 successfully")

    def new_episode(self):
        self.timestep_watch.reset()
        self.env.new_episode()
        self.step_in_an_episode = 0
        for agent in self.agent_list:
            agent.begin_episode()
            if agent.is_prey:
                self.env.player_list[agent.player_idx].is_prey = True
            if agent.is_DQN:
                self.logger.warning("agent: {} in control of player {}".format(agent.player_idx,
                                    self.env.player_list[agent.player_idx].idx))

    def move(self, agent, running, verbose):
        """
        Move the training/evaluation/testing step forward
        :param agent: the agent that will make the action
        :param running: whether the agent will continue running next episode
        :param verbose: Training   -> 1
                        Evaluation -> 2
                        Testing    -> 3
        :return:
        """
        assert verbose in [1, 2, 3]
        agent.step = self.step
        agent.step_in_an_episode = self.step_in_an_episode
        observation = self.env.player_list[agent.player_idx].convert_observation_to_rgb()
        agent.action = agent.act(observation)
        agent.action_stats[agent.action] += 1
        # Log position stats
        # agent.position_stats[self.env.player_list[agent.player_idx].position.y,
        #                     self.env.player_list[agent.player_idx].position.x] += 1
        self.env.take_action(agent.action, self.env.player_list[agent.player_idx])
        self.env.move(agent.step_in_an_episode)
        cur_reward = self.env.player_list[agent.player_idx].reward
        agent.total_reward += cur_reward
        if agent.is_DQN:
            term = not running
            agent.learn(cur_reward, term)
            # Log of DQN training information
            if self.step_in_an_episode % DQNSetting.LOG_FRE == 0:
                if verbose == 1:
                    self.logger.warning("       Agent    ID: {}".format(agent.player_idx))
                    if not agent.is_DRUQN:
                        self.logger.warning("       Training stats @ step {0}|    epsilon:   {1:.3f}".format(agent.step,
                                                                                                            agent.eps) +
                                            "    total_reward:     {}".format(agent.total_reward))
                    else:
                        self.logger.warning("       Training stats @ step {0}|    epsilon:   {1:.3f}".format(agent.step,
                                                                                                agent.eps) +
                                            "    eff_lr:   {0:.4f}".format(agent.eff_lr) +
                                            "    total_reward:  {}".format(agent.total_reward))
                elif verbose == 2:
                    self.logger.warning("       Agent    ID: {}".format(agent.player_idx) +
                                        "       Evaluating stats|  total_reward:     {}".format(agent.total_reward))
                else:
                    self.logger.warning("       Agent    ID: {}".format(agent.player_idx)+
                                        "       Testing stats|  total_reward:     {}".format(agent.total_reward))

    def train_episode(self):
        """ Train the DQN player for a single episode. """
        self.fps_clock = pygame.time.Clock()

        # Initialize the environment.
        self.new_episode()

        # Main game loop.
        running = True
        while running:
            self.step_in_an_episode += 1  # From 1 to self.n_steps
            self.step += 1
            if self.step_in_an_episode == self.n_steps:
                running = False
            # Log of overall information
            if self.step_in_an_episode % DQNSetting.LOG_FRE == 0:
                self.logger.warning("Training Report   @ EPISODE: " + str(self.episode) +
                                    " | STEP: " + str(self.step_in_an_episode) +
                                    " | TOTAL STEP: " + str(self.step) +
                                    " | Elapsed Time: " + str(time.time() - self.start_time))

            agent = self.agent_list[0]
            self.move(agent, running, 1)
            if self.visual:
                self.draw_all_cells()
                pygame.display.update()

            agent = self.agent_list[1]
            self.move(agent, running, 1)
            if self.visual:
                self.draw_all_cells()
                pygame.display.update()
            self.fps_clock.tick(GameSetting.FPS_LIMIT)

    def fit_model(self):
        self.logger.warning("<=====================  Reporting Training Settings  ========================>")
        self.logger.warning("Learning rate: {}".format(DQNSetting.LR))
        self.logger.warning("eps_start: {} | eps_end: {} | eps_decay {} | eps_eval: {}".format(DQNSetting.EPS_START,
                                                                                               DQNSetting.EPS_END,
                                                                                               DQNSetting.EPS_DECAY_LEN,
                                                                                               DQNSetting.EPS_EVAL))
        self.logger.warning("evaluation frequency: {} | evaluation number of episode: {}".format(DQNSetting.EVAL_FRE,
                                                                                            DQNSetting.EVAL_EPISODES))
        self.logger.warning("Learning start at: {} steps".format(DQNSetting.LEARNING_START_IN_EPISODE))
        self.logger.warning("Random seed: {}".format(DQNSetting.SEED))
        self.logger.warning("<============================  Reporting ends  ==============================>")

        self.reset_stats()
        self.episode = 0
        while self.episode < self.n_episodes:
            self.episode += 1
            self.train_episode()
            self.logger.warning("Episode report  @ EPISODE: " + str(self.episode))
            for agent in self.agent_list:
                self.logger.warning("       Agent   ID: {}".format(agent.player_idx))
                self.logger.warning("Training @ episode: {} | total reward:  {}".format(self.episode,
                                                                                                agent.total_reward))
                # self.logger.warning("        Position distribution:" + "\n" + agent.display_position_stats())
                # self.logger.warning("Training @ episode: {} | Action distribution:".format(self.episode)
                #                     + agent.display_action_stats())
            if self.episode % DQNSetting.EVAL_FRE == 0 and self.step > DQNSetting.LEARNING_START_IN_EPISODE:
                self.set_all_agents_to_train(False)
                self.logger.warning("<============  Evaluating starting    @ EPISODE: " + str(self.episode) +
                                    "==============>")
                self.evaluate_episode()
                self.set_all_agents_to_train(True)
                self.logger.warning("<============  Resume training @ EPISODE: {}  ============>".format(self.episode))

            if self.episode % DQNSetting.SAVE_FRE == 0:
                # save stats for all episodes
                for agent in self.agent_list:
                    result = dict()
                    result["reward"] = agent.reward_log
                    result["action_pre"] = agent.action_log
                    result["v_avg"] = agent.v_avg_log
                    result["td_err"] = agent.tderr_avg_log
                    result["reward_avg"] = agent.reward_avg_log
                    pickle.dump(result, open(SaveSetting().RESULT_NAME + "_id-" + str(agent.player_idx) +
                                             "_episode-" + str(self.episode) + ".p", "wb"))
                    del result
                    torch.save(agent.q_network.state_dict(), SaveSetting().MODEL_NAME + "_id-" + str(agent.player_idx) +
                               "_episode-" + str(self.episode) + "_final" + ".pth")
                self.logger.warning("Saving all results successfully @ EPISODE: {}".format(self.episode))


    def evaluate_episode(self):
        """
        evaluate for an episode
        """
        episode_in_eval = 0
        while episode_in_eval < DQNSetting.EVAL_EPISODES:
            episode_in_eval += 1
            self.logger.warning("<=================  In the {} episode of evaluation"
                                "  =================>".format(episode_in_eval))
            self.fps_clock = pygame.time.Clock()

            # Initialize the environment.
            self.new_episode()

            # Main game loop.
            running = True
            while running:
                self.step_in_an_episode += 1  # From 1 to self.n_steps
                if self.step_in_an_episode == self.eval_steps:
                    running = False

                # Log of overall information
                if self.step_in_an_episode % DQNSetting.LOG_FRE == 0:
                    self.logger.warning("Evaluating Report   @ EPISODE: " + str(self.episode) +
                                        " | STEP: " + str(self.step_in_an_episode) +
                                        " | Elapsed Time: " + str(time.time() - self.start_time))

                agent = self.agent_list[0]
                self.move(agent, running, 2)
                if self.visual:
                    self.draw_all_cells()
                    pygame.display.update()

                agent = self.agent_list[1]
                self.move(agent, running, 2)
                if self.visual:
                    self.draw_all_cells()
                    pygame.display.update()
                self.fps_clock.tick(GameSetting.FPS_LIMIT)

            for agent in self.agent_list:
                if agent.is_DQN:
                    v_avg, tderr_avg = agent.compute_validation_stats()
                    agent.v_avg_log.append([self.episode, v_avg])
                    agent.tderr_avg_log.append([self.episode, tderr_avg.data.clone().mean()])
                    agent.reward_log.append([self.episode, agent.total_reward])
                    agent.action_log.append([self.episode, agent.action_stats])
                    self.logger.warning("Evaluation Report for Agent ID: {} @ EPISODE: {}".format(agent.player_idx,
                                                                                                  self.episode))
                    self.logger.warning("       Evaluation @ EPISODE: {0:}| v_avg: {1:.4f} "
                                        "| td_err_avg: {2:.4f}"
                                        "| reward_avg: {3:}"
                                        "| Action distribution|".format(self.episode,
                                                                        agent.v_avg_log[-1][1],
                                                                        agent.tderr_avg_log[-1][1],
                                                                        agent.total_reward) +
                                        agent.display_action_stats())

        for agent in self.agent_list:
            if agent.is_DQN:
                mean_total_reward = np.mean(np.asarray(agent.reward_log)[-DQNSetting.EVAL_EPISODES:, 1])
                agent.reward_avg_log.append([self.episode, mean_total_reward])
                self.logger.warning("<===================  Evaluation stops @ EPISODE: {}| total_avg_reward: {}"
                                    "  ===================>".format(self.episode,mean_total_reward))
                if mean_total_reward >= agent.best_avg_reward and mean_total_reward > 0:
                    agent.best_avg_reward = mean_total_reward
                    torch.save(agent.q_network.state_dict(), SaveSetting().MODEL_NAME + "_id-" + str(agent.player_idx) +
                               "_episode-" + str(self.episode) + "_best" + ".pth")
                    self.logger.warning("Saved  Model for agent ID: {} @ Episode: {}".format(agent.player_idx,
                                                                                             self.episode) +
                                        " | Best Reward: " + str(agent.best_avg_reward))

    def test_model(self):
        self.load_model()
        self.set_all_agents_to_train(False)
        self.reset_stats()
        self.episode = 0
        for agent in self.agent_list:
            agent.learning_start = 0
        log_avg_reward_0 = []
        log_avg_reward_1 = []
        while self.episode < DQNSetting.TEST_EPISODES:
            self.episode += 1
            self.logger.warning("<=================  In the {} episode of Testing"
                                "  =================>".format(self.episode))
            self.step += 1
            self.fps_clock = pygame.time.Clock()

            # Initialize the environment.
            self.new_episode()

            # Main game loop.
            running = True
            while running:
                self.step_in_an_episode += 1  # From 1 to self.n_steps
                if self.step_in_an_episode == self.eval_steps:
                    running = False

                # Log of overall information
                if self.step_in_an_episode % DQNSetting.LOG_FRE == 0:
                    self.logger.warning("Testing Report   @ EPISODE: " + str(self.episode) +
                                        " | STEP: " + str(self.step_in_an_episode) +
                                        " | Elapsed Time: " + str(time.time() - self.start_time))

                agent = self.agent_list[0]
                self.move(agent, running, 3)
                if self.visual:
                    self.draw_all_cells()
                    pygame.display.update()

                agent = self.agent_list[1]
                self.move(agent, running, 3)
                if self.visual:
                    self.draw_all_cells()
                    pygame.display.update()
                self.fps_clock.tick(GameSetting.FPS_LIMIT)

            for agent in self.agent_list:
                if agent.is_DQN:
                    agent.reward_log.append([self.episode, agent.total_reward])
                    agent.action_log.append([self.episode, agent.action_stats])
                    self.logger.warning("Test Report for Agent ID: {} @ EPISODE: {}".format(agent.player_idx,
                                                                                                  self.episode))
                    self.logger.warning("       Test @ EPISODE: {0:}| "
                                        "| reward_avg: {1:}".format(self.episode,
                                                                    agent.total_reward))
                    self.logger.warning("       Action distribution: " + agent.display_action_stats())
            for agent in self.agent_list:
                if agent.is_DQN:
                    mean_total_reward = np.mean(np.asarray(agent.reward_log)[:, 1])
                    self.logger.warning("<===================  Testing @ EPISODE: {}| total_avg_reward: {}"
                                        "  ===================>".format(self.episode, mean_total_reward))

    def reset_stats(self):
        for agent in self.agent_list:
            if agent.is_DQN:
                # log agent information
                agent.v_avg_log = []
                agent.tderr_avg_log = []
                agent.reward_log = []
                agent.action_log = []
                agent.best_avg_reward = 0
                agent.reward_avg_log = []

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

    def set_all_agents_to_train(self, train=True):
        for agent in self.agent_list:
            if agent.is_DQN:
                agent.training = train
