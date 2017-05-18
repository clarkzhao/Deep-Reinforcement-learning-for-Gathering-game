from .utility import *


class CellType(object):
    """ Defines all types of cells that can be found in the game. """

    EMPTY = 0
    APPLE = 1
    PLAYER = 2
    PLAYER_FRONT = 3
    WALL = 4


class Colors:

    SCREEN_BACKGROUND = (10, 10, 10)  # BLACK
    CELL_TYPE = {
        CellType.WALL: (150, 150, 150),  # GRAY
        CellType.PLAYER_FRONT: (50, 50, 50),  # DARK GRAY
        CellType.PLAYER: (0, 0, 255),  # BLUE
        CellType.APPLE: (0, 255, 0),  # GREEN
    }


class PlayerDirection(object):
    """ Defines all possible directions the snake can take, as well as the corresponding offsets. """

    NORTH = Point(0, -1)
    EAST = Point(1, 0)
    SOUTH = Point(0, 1)
    WEST = Point(-1, 0)


class PlayerAction(object):
    STEP_FORWARD = 0
    STEP_BACKWARD = 1
    STEP_LEFT = 2
    STEP_RIGHT = 3
    USE_BEAM = 4
    ROTATE_CLOCKWISE = 5
    ROTATE_COUNTERCLOCKWISE = 6
    STAND_STILL = 7

ALL_PLAYER_DIRECTIONS = [
    PlayerDirection.NORTH,
    PlayerDirection.EAST,
    PlayerDirection.SOUTH,
    PlayerDirection.WEST,
]

ALL_PLAYER_ACTIONS = [
    PlayerAction.STEP_FORWARD,
    PlayerAction.STEP_BACKWARD,
    PlayerAction.STEP_LEFT,
    PlayerAction.STEP_RIGHT,
    PlayerAction.USE_BEAM,
    PlayerAction.ROTATE_CLOCKWISE,
    PlayerAction.ROTATE_COUNTERCLOCKWISE,
    PlayerAction.STAND_STILL,
]


class GameSetting(object):
    FPS_LIMIT = 60
    AI_TIMESTEP_DELAY = 100
    HUMAN_TIMESTEP_DELAY = 500
    CELL_SIZE = 20
    APPLE_RESPAWN_TIME = 3
