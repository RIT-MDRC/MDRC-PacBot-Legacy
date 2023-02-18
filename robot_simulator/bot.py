from grid import *
import math

from bot_math import Pose
from Position import Position
from grid import *


def high_level_strategy(pos: tuple[int, int], direction: int) -> tuple[int, int]:
    """
    Determines the target location based on the current position, direction, and grid state.

    @param pos: The current position of the robot.
    @param direction: The current direction of the robot.
    @param grid: The current shape of the grid.

    @return: The target location.
    """
    pass


def path_finding(pose: Pose, target: Position) -> list[Position]:
    """
    Determines the path to the target location based on the current position, target location, and grid state.

    @param pose: The current position of the robot.
    @param target: The target location.
    @param grid: The current shape of the grid.

    @return: The path to the target location. Only includes endpoints of lines.
    """

    if pose.pos == target:
        return [target]

    # BFS
    return grid_bfs_path(pose.pos, target)


def wheel_control(heading: tuple[float, float]):
    """
    Controls the wheels of the robot based on the desired speed and heading.

    @param heading: The heading of the robot; the magnitude of the values determines the speed, the ratio determines the angle.
    """
    pass
