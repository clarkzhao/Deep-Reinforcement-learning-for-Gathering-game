from constant import *

class Player:
    def __init__(self, row, col, reward = 0):
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
        self.reward = 0

        # a 16x21 grid
        # self.view = view

    def move(self):
        """move the player"""

        # Move left/right
        self.row += self.delta_row

        # Avoid being outside the grid world
        if self.row < 0:
            self.row = 0
        if self.row > ROW_COUNT - 1:
            self.row = ROW_COUNT - 1

        #Move up/down
        self.col += self.delta_col

        # Avoid being outside the grid world
        if self.col < 0:
            self.col = 0
        if self.col > COLUMN_COUNT - 1:
            self.col = COLUMN_COUNT - 1