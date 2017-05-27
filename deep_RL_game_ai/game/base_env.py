import random
from .grid import *
from .player import *
from .apple import *


class EnvironmentBase(object):
    def __init__(self, config):
        self.grid = Grid(game_map=config['grid'])
        self.view_array = None
        self.player_list = []
        self.rewards = config['rewards']
        self.max_step_limit = config.get('max_step_limit', 1000)
        self.is_game_over = False
        self.time_watch = Stopwatch()
        # self.current_action = None
        # self.stats = EpisodeStatistics()
        # self.debug_file = None
        # self.stats_file = None

    def seed(self, value):
        """ Initialize the random state of the environment to make results reproducible. """
        random.seed(value)
        np.random.seed(value)

    @property
    def num_actions(self):
        """ Get the number of actions the agent can take. """
        return len(ALL_PLAYER_ACTIONS)

    def new_episode(self):
        pass

    def get_states(self):
        return self.grid.get_grid()

    def take_action(self, action, player: Player):
        """
        the action is taken and the next position/direction of the player is defined here
        but they will be changed in further methods 
        """
        # self.current_action = action
        if not player.is_tagged:
            if action == PlayerAction.USE_BEAM:
                player.use_beam()

            elif action == PlayerAction.STEP_FORWARD:
                player.step_forward()

            elif action == PlayerAction.STEP_BACKWARD:
                player.step_backward()

            elif action == PlayerAction.STEP_LEFT:
                player.step_left()

            elif action == PlayerAction.STEP_RIGHT:
                player.step_right()

            elif action == PlayerAction.ROTATE_CLOCKWISE:
                player.rotate_clockwise()

            elif action == PlayerAction.ROTATE_COUNTERCLOCKWISE:
                player.rotate_counterclockwise()

            else:
                player.stand_still()

    def update_grid(self, player: Player):
        pass

    def move(self, player: Player):
        pass

    def convert_view(self):
        raise NotImplementedError



