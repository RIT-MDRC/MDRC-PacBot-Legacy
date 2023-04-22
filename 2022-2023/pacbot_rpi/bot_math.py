import math
import random

from typing import NamedTuple




class Position(NamedTuple):
    x: float  # to the right
    y: float  # up

    def dist(self, pos: "Position") -> float:
        return math.hypot(self.x - pos.x, self.y - pos.y)

    def apply_change(self, other: "Position") -> "Position":
        self.x += other.x
        self.y += other.y
        return self


class Pose(NamedTuple):
    pos: Position
    angle: float  # radians, with 0 to the right

    def dist(self, other: "Pose") -> float:
        return self.pos.dist(other.pos)

    def apply_change(self, other: "Pose") -> "Pose":
        self.pos.apply_change(other.pos)
        self.angle += other.angle
        return self


from grid import get_grid_open_spaces

sorted_spaces = get_grid_open_spaces()
NUM_PF_POINTS = 1_000

POS_ESTIMATE_VARIABILITY = 5
ANGLE_ESTIMATE_VARIABILITY = math.pi


def normalize_angle(angle: float) -> float:
    """Normalizes an angle to be between -pi and pi radians."""
    return (angle + math.pi) % (2 * math.pi) - math.pi


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
