from game.gathering_env import *
from .base_gui import *

import json
import pygame


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
