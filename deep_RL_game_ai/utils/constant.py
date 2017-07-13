from .utility import *
import os
import datetime

class CellType(object):
    """ Defines all types of cells that can be found in the game. """

    EMPTY = 0
    APPLE = 1
    PLAYER = 2
    PLAYER_FRONT = 3
    WALL = 4
    BEAM = 5
    OPPONENT = 6
    AGENT = 7

class Colors:

    SCREEN_BACKGROUND = (10, 10, 10)  # BLACK
    CELL_TYPE = {
        CellType.WALL: (125, 125, 125),  # GRAY
        CellType.PLAYER_FRONT: (50, 50, 50),  # DARK GRAY
        CellType.PLAYER: (0, 0, 255),  # BLUE
        CellType.AGENT: (0, 0, 255),  # BLUE
        CellType.OPPONENT: (255, 0, 0),  # RED
        CellType.APPLE: (0, 255, 0),  # GREEN
        CellType.BEAM: (255, 204, 51),  # Yellow
    }


class PlayerDirection(object):
    """ Defines all possible directions the snake can take, as well as the corresponding offsets. """

    NORTH = Point(0, -1)
    EAST = Point(1, 0)
    SOUTH = Point(0, 1)
    WEST = Point(-1, 0)

INITIAL_POSITION_1 = Point(1, 6)
INITIAL_POSITION_2 = Point(31, 6)


class PlayerAction(object):
    STEP_FORWARD = 0
    STEP_BACKWARD = 1
    STEP_LEFT = 2
    STEP_RIGHT = 3
    USE_BEAM = 4
    ROTATE_CLOCKWISE = 5
    ROTATE_COUNTERCLOCKWISE = 6
    STAND_STILL = 7

    @staticmethod
    def to_string(a):
        return {
            0: 'STEP FORWARD',
            1: 'STEP BACKWARD',
            2: 'STEP LEFT',
            3: 'STEP RIGHT',
            4: 'USE BEAM',
            5: 'ROTATE CLOCKWISE',
            6: 'ROTATE COUNTERCLOCKWISE',
            7: 'STAND STILL'}[a]

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

ALL_PREY_ACTIONS = [
    PlayerAction.STEP_FORWARD,
    PlayerAction.STEP_BACKWARD,
    PlayerAction.STEP_LEFT,
    PlayerAction.STEP_RIGHT,
    PlayerAction.ROTATE_CLOCKWISE,
    PlayerAction.ROTATE_COUNTERCLOCKWISE,
    PlayerAction.STAND_STILL,
]


class GameSetting(object):
    FPS_LIMIT = 60
    AI_TIMESTEP_DELAY = 1
    HUMAN_TIMESTEP_DELAY = 200
    CELL_SIZE = 20
    APPLE_RESPAWN_TIME = 1000  # milliseconds
    TAGGED_TIME = 1000  # milliseconds
    player_view = [16, 21]
    BEAM_DURATION = 10
    GUI = True
    AGENT_VIEW_RANGE = [16, 21]


class DQNSetting(object):
    EPS_START = 1.0  # epsilon at the start
    EPS_END = 0.1  # epsilon in the end
    EPS_DECAY_LEN = 1000000  # number of steps for the epsilon to decay
    EPS_EVAL = 0.  # epsilon for evaluation
    GAMMA = 0.99  # discounted factor
    MEMORY_SIZE = int(1e5)  # size of replay buffer
    N_COLS = 3  # number of color channels in the input
    N_HIST = 1  # length of history
    BATCH_SIZE = 32  # how many transitions to sample each time from the memory buffer in training
    VALID_SIZE = 500  # how many transitions to sample each time from the memory buffer in validation
    TARGET_UPDATE_FRE = 1000  # how many steps to update the target Q networks
    TOTAL_STEPS_PER_EPISODE = 1000  # how many steps in an episode
    TOTAL_NUM_EPISODE = 2000  # how many number of episode to train on
    EVAL_FRE = 5  # the evaluation frequency in number of episode, evaluate once for every 'EVAL_FRE' episodes
    LOG_FRE = 100  # how many steps to display the training information
    EVAL_STEPS = 1000  # how many steps for evaluation
    LEARNING_START_IN_EPISODE = 5000  # how many steps does the learning start in the first episode
    VISUAL_GUI = False  # whether or not to render the game
    CLIP_GRAD = 40.
    VISUAL_DATA = True
    SAVE_FRE = 100

    # Change for DQN or DRUQN
    LR = 0.0005  # learning rate
    ALPHA = 0.01

    # File name for the saved DQN model
    PRETRAINED_MODEL_1 = ""
    PRETRAINED_MODEL_2 = ""

GAME_CONTROL_KEYS = [
    pygame.K_UP,
    pygame.K_LEFT,
    pygame.K_DOWN,
    pygame.K_RIGHT,
    pygame.K_o,
    pygame.K_p,
    pygame.K_SPACE,
    pygame.K_z
]

GAME_CONTROL_KEYS_2 = [
    pygame.K_w,
    pygame.K_a,
    pygame.K_s,
    pygame.K_d,
    pygame.K_q,
    pygame.K_e,
    pygame.K_j,
    pygame.K_k
]


class SaveSetting(object):
    def __init__(self):
        self.root_dir = os.getcwd()
        self.timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
        self.MODEL_NAME = self.root_dir + "/output/saved_models/" + self.timestamp
        self.RESULT_NAME = self.root_dir + "/output/results/" + self.timestamp


class Params(object):
    def __init__(self):
        self.root_dir = os.getcwd()
        self.timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
        self.log_name = self.root_dir + "/logs/" + self.timestamp + ".log"
        self.logger = loggerConfig(self.log_name)
        self.logger.warning("<===================================>")
