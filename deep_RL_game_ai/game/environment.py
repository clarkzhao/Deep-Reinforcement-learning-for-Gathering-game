import random
from .grid import *
from .player import *
from .apple import *


class Environment(object):

    def __init__(self, config):
        self.grid = Grid(game_map=config['grid'])
        self.player = None
        self.apple_list = None
        self.rewards = config['rewards']
        self.max_step_limit = config.get('max_step_limit', 1000)
        self.is_game_over = False

        self.timestep_index = 0
        self.total_time_in_episode = 0.
        self.current_action = None
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
        """Reset the environment and begin a new episode"""
        self.grid.create_grid()
        # self.stats.reset()
        self.timestep_index = 0
        self.total_time_in_episode = 0.
        self.player = Player(self.grid.find_player())
        self.grid.place_player(self.player)
        self.current_action = None
        self.is_game_over = False
        # self.generate_apples()

    def choose_action(self, action):
        """
        the action is taken and the next position/direction of the player is defined here
        but they will be changed in further methods 
        """
        self.current_action = action
        if action == PlayerAction.USE_BEAM:
            self.player.use_beam()
            # next_direction = self.player.direction

        elif action == PlayerAction.STEP_FORWARD:
            self.player.step_forward()
            # next_direction = self.player.direction

        elif action == PlayerAction.STEP_BACKWARD:
            self.player.step_backward()
            # next_direction = self.player.direction

        elif action == PlayerAction.STEP_LEFT:
            self.player.step_left()
            # next_direction = self.player.direction

        elif action == PlayerAction.STEP_RIGHT:
            self.player.step_right()
            # next_direction = self.player.direction

        elif action == PlayerAction.ROTATE_CLOCKWISE:
            self.player.rotate_clockwise()
            # next_position = self.player.position

        elif action == PlayerAction.ROTATE_COUNTERCLOCKWISE:
            self.player.rotate_counterclockwise()
            # next_position = self.player.position

        else:
            self.player.stand_still()

    def update_grid(self):
        """
        In this method, we assume the next position/direction of the player
        is correct
        """
        # Clear the cell for the front of the player
        if self.grid[self.player.current_front] == CellType.PLAYER_FRONT:
            self.grid[self.player.current_front] = CellType.EMPTY

        # Clear the cell for the current position of the player
        self.grid[self.player.position] = CellType.EMPTY

        # Move the player
        self.player.move()

        # Place the player in the new position
        self.grid.place_player(self.player)

    def move(self):
        """
        In this method, the player is moved to the next position it should be 
        Any reward and beam detection is happened here
        """
        self.timestep_index += 1

        # if the next position is the wall
        # the player is forced back to the current position
        if self.grid[self.player.next_position] in [CellType.WALL]:
            self.player.next_position = self.player.position

        # if the next position is outside the 2D grid
        # the player is forced to be on the edge of the grid
        if self.player.next_position.x < 0:
            self.player.next_position.x = 0
        elif self.player.next_position.x >= self.grid.width:
            self.player.next_position.x = self.grid.width - 1
        if self.player.next_position.y < 0:
            self.player.next_position.y = 0
        elif self.player.next_position.y >= self.grid.width:
            self.player.next_position.y = self.grid.height - 1

        self.update_grid()
