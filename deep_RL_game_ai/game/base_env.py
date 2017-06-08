import random
from .grid import *
from .player import *
from .apple import *
from utils.constant import PlayerDirection
from utils.utility import TimestepResult

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

    def convert_view(self, input_player: Player):
        """Convert the player cells in grid to a specified player's perspective"""
        self.view_array = self.grid.copy_cells()
        for player in self.player_list:
            if not player.is_tagged:
                if player is input_player:
                    self.view_array[player.position.y, player.position.x] = CellType.AGENT
                else:
                    self.view_array[player.position.y, player.position.x] = CellType.OPPONENT

    def get_observation(self):
        # grid = self.grid.copy_cells()
        for player in self.player_list:
            self.convert_view(player)
            grid = self.view_array
            observation = np.zeros(GameSetting.player_view, 'int8')
            if player.direction == PlayerDirection.NORTH:
                x_min = 0 if player.position.x - 10 < 0 else player.position.x - 10
                x_max = self.grid.width - 1 if player.position.x + 10 > self.grid.width - 1 \
                    else player.position.x + 10
                y_min = 0 if player.position.y - 15 < 0 else player.position.y
                y_max = player.position.y
                area = grid[y_min:y_max + 1, x_min:x_max + 1]
                observation[16 - area.shape[0]:, 10 - (player.position.x - x_min):10 + (x_max - player.position.x) + 1] = area

            elif player.direction == PlayerDirection.SOUTH:
                x_min = 0 if player.position.x - 10 < 0 else player.position.x - 10
                x_max = self.grid.width - 1 if player.position.x + 10 > self.grid.width - 1 \
                    else player.position.x + 10
                y_min = player.position.y
                y_max = self.grid.height - 1 if player.position.y + 15 > self.grid.height - 1 \
                    else player.position.y + 15
                area = grid[y_min:y_max + 1, x_min:x_max + 1]
                area = np.rot90(area, 2)
                observation[16 - area.shape[0]:, 10 - (x_max - player.position.x):10 + (player.position.x - x_min) + 1] = area

            elif player.direction == PlayerDirection.WEST:
                x_min = 0 if player.position.x - 15 < 0 else player.position.x - 15
                x_max = player.position.x
                y_min = 0 if player.position.y - 10 < 0 else player.position.y - 10
                y_max = self.grid.height - 1 if player.position.y + 10 > self.grid.height - 1 \
                    else player.position.y + 10
                area = grid[y_min:y_max + 1, x_min:x_max + 1]
                area = np.rot90(area, 3)
                observation[16 - area.shape[0]:, 10 - (y_max - player.position.y):10 + (player.position.y - y_min) + 1] = area

            else:
                x_min = player.position.x
                x_max = self.grid.width - 1 if player.position.x + 15 > self.grid.width - 1 \
                    else player.position.x + 15
                y_min = 0 if player.position.y - 10 < 0 else player.position.y - 10
                y_max = self.grid.height - 1 if player.position.y + 10 > self.grid.height - 1 \
                    else player.position.y + 10
                area = grid[y_min:y_max + 1, x_min:x_max + 1]
                area = np.rot90(area, 1)
                observation[16 - area.shape[0]:, 10 - (player.position.y - y_min):10 + (y_max - player.position.y) + 1] = area

            player.observation = observation

    def update_front_of_players(self):
        # After clear all beams in the grid,
        # the front of the player is cleared as well.
        # To make the front of the player back to the grid,
        # This method is called after clearing the beam area
        for player in self.player_list:
            if not player.is_tagged:
                self.grid.place_player(player)
