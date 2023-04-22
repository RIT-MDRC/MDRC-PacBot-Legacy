import math
from sim_canvas import world2screen, COLOR_ROBOT, ROBOT_RADIUS
import pygame as pg
import os

from bot_math import Pose, Position

MAX_WHEEL_SPEED = float(os.environ.get("MAX_WHEEL_SPEED", "5.0"))
DIST_BETWEEN_WHEELS = 4.0 / 3.5


class Robot:
    def __init__(self):
        # self.pose = Pose(Position(14, 7), 0.0)  # radians
        self.pose = Pose(Position(4, 29), math.pi)  # radians

    def step(self, left_motor, right_motor, dt):
        """
        left_motor and right_motor are in the range [-1.0, +1.0].
        dt is the time step in seconds.
        """
        left_wheel = min(max(left_motor, -1.0), +1.0) * MAX_WHEEL_SPEED
        right_wheel = min(max(right_motor, -1.0), +1.0) * MAX_WHEEL_SPEED
        linear_speed = (left_wheel + right_wheel) / 2
        angular_speed = (left_wheel - right_wheel) / DIST_BETWEEN_WHEELS

        self.pose = Pose(
            Position(
                self.pose.pos.x + linear_speed * dt * math.cos(self.pose.angle),
                self.pose.pos.y + linear_speed * dt * math.sin(self.pose.angle),
            ),
            self.pose.angle + angular_speed * dt,
        )

    def draw(self, surface):
        center = world2screen((self.pose.pos.x, self.pose.pos.y))

        pg.draw.circle(surface, COLOR_ROBOT, center, ROBOT_RADIUS, width=2)
        end_pos = (
            center[0] + math.cos(self.pose.angle) * ROBOT_RADIUS,
            center[1] + math.sin(self.pose.angle) * ROBOT_RADIUS,
        )
        pg.draw.line(surface, COLOR_ROBOT, center, end_pos)