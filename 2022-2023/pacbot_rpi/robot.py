import math

from bot_math import Pose, Position

MAX_WHEEL_SPEED = 10
DIST_BETWEEN_WHEELS = 4.0 / 3.5


class Robot:
    def __init__(self):
        self.pose = Pose(Position(14, 17), 0.0)  # radians

    def step(self, left_motor, right_motor, dt):
        """
        left_motor and right_motor are in the range [-1.0, +1.0].
        dt is the time step in seconds.
        """
        left_wheel = min(max(left_motor, -1.0), +1.0) * MAX_WHEEL_SPEED
        right_wheel = min(max(right_motor, -1.0), +1.0) * MAX_WHEEL_SPEED
        linear_speed = (left_wheel + right_wheel) / 2
        angular_speed = (left_wheel - right_wheel) / DIST_BETWEEN_WHEELS

        self.pose.angle += angular_speed * dt
        self.pose.pos.x += linear_speed * dt * math.cos(self.pose.angle)
        self.pose.pos.y += linear_speed * dt * math.sin(self.pose.angle)
