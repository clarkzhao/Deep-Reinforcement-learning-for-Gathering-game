from collections import namedtuple
import pygame


class Point(namedtuple('PointTuple', ['x', 'y'])):
    """
        A 2D point class with named axis: 'x' and 'y'.
    """

    def __add__(self, p):
        """ Add two points. """
        return Point(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        """ Subtract two points. """
        return Point(self.x - p.x, self.y - p.y)


class Stopwatch(object):
    """ Measures the time elapsed since the last checkpoint. """

    def __init__(self):
        self.start_time = pygame.time.get_ticks()

    def reset(self):
        """ Set a new checkpoint. """
        self.start_time = pygame.time.get_ticks()

    def time(self):
        """ Get time (in milliseconds) since the last checkpoint. """
        return pygame.time.get_ticks() - self.start_time

class TimestepResult(object):
    """ Represents the information provided to the agent after each timestep. """

    def __init__(self, observation, reward, is_episode_end):
        self.observation = observation
        self.reward = reward
        self.is_episode_end = is_episode_end

    def __str__(self):
        grid_map = '\n'.join([
            ''.join(str(cell) for cell in row)
            for row in self.observation
        ])
        return f'{grid_map}\nR = {self.reward}   end={self.is_episode_end}\n'