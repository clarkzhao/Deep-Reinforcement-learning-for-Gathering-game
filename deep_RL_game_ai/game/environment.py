import random
from .grid import *
from .player import *
from .apple import *


class Environment(object):

    def __init__(self, config):
        self.grid = Grid(game_map=config['grid'])
        self.player = None
        self.player_list = []
        self.apple_list = []
        self.rewards = config['rewards']
        self.max_step_limit = config.get('max_step_limit', 1000)
        self.is_game_over = False
        self.apple_eaten = 0
        self.timestep_index = 0
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
        """Reset the environment and begin a new episode"""
        self.grid.create_grid()
        self.apple_eaten = 0
        # self.stats.reset()
        self.timestep_index = 0
        for point in self.grid.find_player():
            self.player_list.append(Player(point))
        for player in self.player_list:
            self.grid.place_player(player)
        # self.current_action = None
        self.is_game_over = False
        self.generate_apples()
        self.grid.place_apples(self.apple_list)

    def get_states(self):
        return self.grid.get_grid()

    def take_action(self, action, player: Player):
        """
        the action is taken and the next position/direction of the player is defined here
        but they will be changed in further methods 
        """
        # self.current_action = action
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

    def generate_apples(self, size=3, start=np.array([3,6])):
        """
        add apples of the diamond shape with given size
        :param size: the size of diamond
        :param start: the starting point of the diamond in 
                        the left-bottom corner
        :return: the added apple
        """
        l = size * 2 - 1
        top = start + l - 1
        for idx in range(size - 1):
            for i in range(idx * 2 + 1):
                y = top[0] - idx
                x = start[1] + size - 1 - idx + i
                self.apple_list.append(Apple(Point(x, y)))
        for idx in range(size - 1, -1, -1):
            for i in range(idx * 2 + 1):
                y = start[0] + idx
                x = start[1] + size - 1 - idx + i
                self.apple_list.append(Apple(Point(x, y)))

    def update_grid(self, player: Player):
        """
        In this method, we assume the next position/direction of the player
        is valid
        """
        # Clear the cell for the beam
        # self.grid.clear_beam_area()

        # Clear the cell for the front of the player
        if self.grid[player.current_front] == CellType.PLAYER_FRONT:
            self.grid[player.current_front] = CellType.EMPTY

        # Clear the cell for the current position of the player
        self.grid[player.position] = CellType.EMPTY

        # Move the player
        player.move()

        # Place the player in the new position
        self.grid.place_player(player)

        # Place the apples
        self.grid.place_apples(self.apple_list)

        # Update the beam area
        if player.using_beam:
            self.grid.place_beam_area(player)
        # else:
            # self.grid.clear_beam_area()

    def move(self, player: Player):
        """
        In this method, the player is moved to the next position it should be 
        Any reward and beam detection is happened here
        """
        self.timestep_index += 1

        # If any apple can be respawn?
        for apple in self.apple_list:
            if apple.is_collected:
                if self.timestep_index - apple.collected_time \
                 >= GameSetting.APPLE_RESPAWN_TIME:
                    apple.respawn()

        # if the next position is the wall
        # the player is forced back to the current position
        if self.grid[player.next_position] in [CellType.WALL, CellType.PLAYER]:
            player.next_position = player.position

        # if the next position is outside the 2D grid
        # the player is forced to be on the edge of the grid
        if player.next_position.x < 0:
            player.next_position.x = 0
        elif player.next_position.x >= self.grid.width:
            player.next_position.x = self.grid.width - 1
        if player.next_position.y < 0:
            player.next_position.y = 0
        elif player.next_position.y >= self.grid.width:
            player.next_position.y = self.grid.height - 1

        # Update the grid to correct Celltype
        self.update_grid(player)

        # Check if the player is about to collect any apple
        for apple in self.apple_list:
            if not apple.is_collected and apple.position == player.position:
                apple.get_collected(self.timestep_index)
                self.apple_eaten += 1
                print("Apple eaten:", self.apple_eaten)

