import math
import random

from grid import *

sorted_spaces = GRID_OPEN_SPACES


def pf_random_point(pos: [float, float], angle: float, pos_range: int, angle_range: float, robot_radius: float) \
        -> tuple[float, float]:
    """
    Returns a random valid point given the grid.

    @param grid: The current shape of the grid.

    @return: A random point within the grid.
    """

    x, y = sorted_spaces[min(len(sorted_spaces), int(abs(random.normalvariate(0, pos_range))))]
    # return a point within 0.5 units of the selected point, preferring closer points
    return x + random.normalvariate(0, 0.4), y + random.normalvariate(0, 0.4)


def pf_change_position(pos: [float, float]):
    global sorted_spaces
    # sort GRID_OPEN_SPACES array by distance to robot
    sorted_spaces = sorted(sorted_spaces, key=lambda x: dist(pos, x))


def particle_filter(last_pos: tuple[float, float], last_angle: float) -> tuple[float, float]:
    """
    Determines the current position and direction of the robot based on the last known position and angle.

    @param last_pos: The last known position of the robot.
    @param last_angle: The last known direction of the robot.
    @param grid: The current shape of the grid.

    @return: The current position and direction of the robot.
    """
    pass


def get_smooth_acceleration(speed: float, max_speed: float, max_acceleration: float, distance: float) -> float:
    """
    Determines the acceleration of the robot based on the current speed, maximum speed,
    maximum acceleration, and distance.

    @param speed: The current speed of the robot.
    @param max_speed: The maximum speed of the robot.
    @param max_acceleration: The maximum acceleration of the robot.
    @param distance: The distance to the target location.

    @return: The acceleration of the robot.
    """
    pass


def dist(pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
    """
    Determines the distance between two points.

    @param pos1: The first point.
    @param pos2: The second point.

    @return: The distance between the two points.
    """
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
