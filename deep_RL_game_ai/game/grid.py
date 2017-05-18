from utils.constant import *
import numpy as np
from .player import *

class Grid(object):
    """ Represent the playing grid of the game"""

    def __init__(self, game_map=None):
        """
        Create a new game grid.

        :param game_map: a list of strings representing the grid object (one string each row).
        """

        self.game_map = game_map

        # 2D numpy array
        self._cells = None

        self._empty_cells = set()

        self._map_to_cell_type = {
            'P': CellType.PLAYER,
            'f': CellType.PLAYER_FRONT,
            '#': CellType.WALL,
            'A': CellType.APPLE,
            '.': CellType.EMPTY,
        }
        self._cell_type_to_map = {
            cell_type: symbol
            for symbol, cell_type in self._map_to_cell_type.items()
        }

    def __getitem__(self, point):
        x, y = point
        return self._cells[y, x]

    def __setitem__(self, point, cell_type):
        """ Update the type of cell at the given point. """
        x, y = point
        self._cells[y, x] = cell_type

        # Do some internal bookkeeping to not rely on random selection of blank cells.
        if cell_type == CellType.EMPTY:
            self._empty_cells.add(point)
        else:
            if point in self._empty_cells:
                self._empty_cells.remove(point)

    def __str__(self):
        return '\n'.join(
            ''.join(self._cell_type_to_map[cell] for cell in row)
            for row in self._cells
        )

    @property
    def width(self):
        return len(self.game_map[0])

    @property
    def height(self):
        return len(self.game_map)

    def create_grid(self):
        """
        Create the 2D numpy cells from the game map
        """
        self._cells = np.array([
            [self._map_to_cell_type[symbol] for symbol in line]
            for line in self.game_map
        ])

        self._empty_cells = {
            Point(x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self[(x, y)] == CellType.EMPTY
        }

    def return_grid(self):
        """
        :return: The 2d grid 
        """
        return self._cells

    def find_player(self):
        """ 
        Find the snake's head on the field. 
        
        :return: the location of player
        """
        for y in range(self.height):
            for x in range(self.width):
                if self[(x, y)] == CellType.PLAYER:
                    return Point(x, y)

    def place_player(self, player: Player):
        self[player.position] = CellType.PLAYER
        self.update_front_of_player(player)

    def update_front_of_player(self, player):
        front_position = player.current_front
        if self[front_position] not in [CellType.APPLE, CellType.WALL]:
            self[front_position] = CellType.PLAYER_FRONT

    def place_apples(self, apple_list):
        for apple in apple_list:
            if not apple.is_collected:
                if self[apple.position] not in [CellType.PLAYER, CellType.WALL]:
                    self[apple.position] = CellType.APPLE
