import math
import random

from typing import NamedTuple
from grid import *

sorted_spaces = GRID_OPEN_SPACES
NUM_PF_POINTS = 1_000

POS_ESTIMATE_VARIABILITY = 5
ANGLE_ESTIMATE_VARIABILITY = math.pi


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


def normalize_angle(angle: float) -> float:
    """Normalizes an angle to be between -pi and pi radians."""
    return (angle + math.pi) % (2 * math.pi) - math.pi

def pf_random_point(angle: float, pos_range: int, angle_range: float, robot_radius: float = 0.4) \
        -> Pose:
    """
    Returns a random valid point given the grid.

    @param angle: the current angle that the best guess robot is facing
    @param pos_range: new points should be generated among the closest __ spaces around the robot
    @param angle_range: new angles should be generated with a normal distribution using this sigma around angle
    @param robot_radius: the radius of the physical robot, used to prevent generating points inside walls

    @return: A random point within the grid.
    """

    x, y = sorted_spaces[min(len(sorted_spaces), int(abs(random.normalvariate(0, pos_range))))]
    # return a point within 0.5 units of the selected point, preferring closer points
    return Pose(Position(x + random.normalvariate(0, robot_radius), y + random.normalvariate(0, robot_radius)),
                random.normalvariate(angle, angle_range))


def pf_change_position(pos: Position):
    """
    Should be called whenever the robot's position changes and before generating new points

    @param pos: The updated best guess of the robot's position, can be very rough
    """
    global sorted_spaces
    # sort GRID_OPEN_SPACES array by distance to robot
    sorted_spaces = sorted(sorted_spaces, key=lambda x: pos.dist(Position(x[0], x[1])))


PF_POINTS: list[Pose] = []


def particle_filter_setup(pos_initial: Pose) -> None:
    """
    Should be called once before particle_filter is ever called

    @param pos_initial: The initial position of the robot
    """
    global PF_POINTS

    pf_change_position(pos_initial.pos)
    PF_POINTS = [pf_random_point(pos_initial.angle, 5, math.pi) for _ in range(NUM_PF_POINTS)]


def particle_filter(pos_change: Pose, sensor_values: tuple[float, float, float, float, float]) -> Pose:
    """
    Determines the current position and direction of the robot based on the last known position and angle.

    @param pos_change: based on encoders, the estimated change in x, y, and angle of the robot

    @return: The current position and direction of the robot.
    """
    global PF_POINTS

    # apply the change in position to each Pose in PF_POINTS
    for p in PF_POINTS:
        p.apply_change(pos_change)

    # TODO calculate the accuracy of each PF_POINT based on sensor values

    # TODO cull worst points

    # TODO generate new points

    # TODO find best guess position

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
