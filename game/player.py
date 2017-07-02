"""
The player class corresponding to the blue square
in the Gathering game
"""
import constant


class Player:
    def __init__(self, row, col, reward=0):
        """Initialize  our player"""

        # Position
        # row is within the range of [0, ROW_COUNT-1]
        self.row = row
        # col is within the range of [0, COLUMN_COUNT-1]
        self.col = col

        # Vector
        self.delta_row = 0
        self.delta_col = 0

        # Total reward gathered
        self.reward = reward

        # Direction
        self.direction = constant.UP

        # rotate clockwise -> 1
        # rotate counter-clockwise -> -1
        self.delta_direction = 0

        self.use_beam = False
        # a 16x21 grid
        # self.view = view

    def move(self):
        """move the player"""
        # Move left/right
        self.row += self.delta_row

        # Avoid being outside the grid world
        if self.row < 0:
            self.row = 0
        if self.row > constant.ROW_COUNT - 1:
            self.row = constant.ROW_COUNT - 1

        # Move up/down
        self.col += self.delta_col

        # Avoid being outside the grid world
        if self.col < 0:
            self.col = 0
        if self.col > constant.COLUMN_COUNT - 1:
            self.col = constant.COLUMN_COUNT - 1

        # Rotate
        self.direction = (self.direction + self.delta_direction) % 4

    def clear(self):
        self.delta_col = 0
        self.delta_row = 0
        self.delta_direction = 0

    def get_reward(self):
        self.reward += 1
        print("Total reward: ", self.reward)
