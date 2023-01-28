from grid import *


def high_level_strategy(pos: tuple[int, int], direction: int, grid: list[int, int]) -> tuple[int, int]:
    """
    Determines the target location based on the current position, direction, and grid state.

    @param pos: The current position of the robot.
    @param direction: The current direction of the robot.
    @param grid: The current shape of the grid.

    @return: The target location.
    """
    pass


def path_finding(pos: tuple[int, int], target: tuple[int, int], grid: list[int, int]) -> list[tuple[int, int]]:
    """
    Determines the path to the target location based on the current position, target location, and grid state.

    @param pos: The current position of the robot.
    @param target: The target location.
    @param grid: The current shape of the grid.

    @return: The path to the target location. Only includes endpoints of lines.
    """
    pass


def determine_heading(pos: tuple[float, float], angle: float, path: list[tuple[int, int]], grid: list[int, int]) \
        -> tuple[float, float]:
    """
    Determines the heading of the robot based on the current position, direction, path to follow, and grid state.
    Utilizes localization via particle filter and acceleration control via PID controller / trapezoid function.

    @param pos: The current position of the robot.
    @param angle: The current direction of the robot.
    @param path: The path to follow.
    @param grid: The current shape of the grid.

    @return: (speed, angle)  The speed and angle of the robot.
    """
    
    
    
    pass


def wheel_control(heading: tuple[float, float]):
    """
    Controls the wheels of the robot based on the desired speed and heading.

    @param heading: The heading of the robot; the magnitude of the values determines the speed, the ratio determines the angle.
    """
    pass
