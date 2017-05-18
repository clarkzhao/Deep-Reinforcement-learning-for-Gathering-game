from utils.constant import *


class Player(object):
    def __init__(self, start_position):
        """
        Create a new player.

        :param start_position: A point representing the initial position of the player
        """

        self.direction = PlayerDirection.NORTH
        self.directions = ALL_PLAYER_DIRECTIONS
        self.position = Point(start_position.x, start_position.y)
        self.next_position = self.position
        self.next_direction = self.direction
        self.using_beam = False

    @property
    def current_front(self):
        return self.position + self.direction

    @property
    def next_front(self):
        return self.next_position + self.next_direction

    def stand_still(self):
        self.using_beam = False
        pass

    def step_forward(self):
        self.using_beam = False
        self.next_position = self.position + self.direction

    def step_backward(self):
        self.using_beam = False
        self.next_position = self.position - self.direction

    def rotate_clockwise(self):
        self.using_beam = False
        direction_idx = self.directions.index(self.direction)
        self.next_direction = self.directions[(direction_idx + 1) % len(self.directions)]

    def rotate_counterclockwise(self):
        self.using_beam = False
        direction_idx = self.directions.index(self.direction)
        self.next_direction = self.directions[(direction_idx - 1) % len(self.directions)]

    def step_left(self):
        self.using_beam = False
        direction_idx = self.directions.index(self.direction)
        direction = self.directions[(direction_idx - 1) % len(self.directions)]
        self.next_position = self.position + direction

    def step_right(self):
        self.using_beam = False
        direction_idx = self.directions.index(self.direction)
        direction = self.directions[(direction_idx + 1) % len(self.directions)]
        self.next_position = self.position + direction

    def move(self):
        self.position = self.next_position
        self.direction = self.next_direction

    def use_beam(self):
        self.using_beam = True

    def is_position_moved(self):
        if self.next_position != self.position:
            return True
        else:
            return False

    def is_direction_moved(self):
        if self.next_direction != self.direction:
            return True
        else:
            return False
