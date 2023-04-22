from bot_math import Pose, Position
import pacbot_rs
import pygame as pg
from grid import GRID_WIDTH, GRID_HEIGHT, GRID
import math

DRAW_SCALE = 30

SCREENRECT = pg.Rect(
    0, 0, (GRID_WIDTH + 2) * DRAW_SCALE, (GRID_HEIGHT + 2) * DRAW_SCALE
)
COLOR_BG = (255, 255, 255)
COLOR_LINE = (0, 0, 0)
COLOR_WALL_FILL = (192, 192, 192)
COLOR_ROBOT = (0, 0, 255)
COLOR_RAY = (255, 0, 0)
COLOR_RAY_MAXED = (0, 200, 0)

FPS = 60

ROBOT_RADIUS = DRAW_SCALE * (6 / 3.5) / 2
SENSOR_ANGLES = [-math.pi / 2, -math.pi / 4, 0, +math.pi / 4, +math.pi / 2]


def world2screen(world_pos: tuple[float, float]) -> tuple[float, float]:
    """Convert world coordinates to screen coordinates."""
    wx, wy = world_pos
    return ((wx + 1) * DRAW_SCALE, (wy + 1) * DRAW_SCALE)


from robot import Robot


def get_alt_grid():
    alt_grid = [[True] * (GRID_HEIGHT + 1) for _ in range(GRID_WIDTH + 1)]
    for x in range(GRID_WIDTH - 1):
        for y in range(GRID_HEIGHT - 1):
            alt_grid[x + 1][y + 1] = (
                    GRID[x][y] and GRID[x + 1][y] and GRID[x][y + 1] and GRID[x + 1][y + 1]
            )
    return alt_grid


class SimCanvas:
    def __init__(self, game_state: pacbot_rs.GameState, particle_filter: pacbot_rs.ParticleFilter):
        self.game_state = game_state
        self.particle_filter = particle_filter

        pg.display.init()

        winstyle = 0  # |FULLSCREEN

        bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
        self.display = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

        self.background_image = pg.Surface(SCREENRECT.size).convert()
        self.bg_rect = self.background_image.get_rect(
            center=(SCREENRECT.width // 2, SCREENRECT.height // 2)
        )

        # fill the background color
        pg.draw.rect(self.background_image, COLOR_BG, self.bg_rect)

        # fill the walls
        alt_grid = get_alt_grid()
        for x in range(GRID_WIDTH + 1):
            for y in range(GRID_HEIGHT + 1):
                if alt_grid[x][y]:
                    rect = pg.Rect(*world2screen((x - 1, GRID_HEIGHT - y - 1)), DRAW_SCALE, DRAW_SCALE)
                    pg.draw.rect(self.background_image, COLOR_WALL_FILL, rect)

        pg.display.flip()

    def update(self, game_state: pacbot_rs.GameState, particle_filter: pacbot_rs.ParticleFilter, robot: Robot,
               destination: (int, int), test_path: list[Position]):
        self.game_state = game_state
        self.particle_filter = particle_filter

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                elif event.key == pg.K_f:
                    pass  # ...

            # clear / draw the background
        self.display.blit(self.background_image, self.bg_rect)

        # draw the robot
        robot.draw(self.display)
        robot_pose = particle_filter.get_pose()
        # robot2 is the particle filter's idea of where the robot is
        robot2 = Robot()
        robot2.pose = Pose(
            Position(robot_pose[0][0], robot_pose[0][1]),
            robot_pose[1]
        )
        robot2.draw(self.display)
        # this dot represents the robot's destination
        pg.draw.circle(self.display, (0, 255, 0), world2screen((destination[0], destination[1])), 5)
        for i in range(5):
            angle = SENSOR_ANGLES[i]
            distance = particle_filter.get_sense_distances()[i]
            # draw line from pacbot to the sensed wall
            pg.draw.line(self.display, COLOR_RAY, world2screen(robot_pose[0]), world2screen(
                (robot_pose[0][0] + distance * math.cos(robot_pose[1] + angle),
                 robot_pose[0][1] + distance * math.sin(robot_pose[1] + angle))), 2)

        for (x1, x2, y1, y2) in particle_filter.get_map_segments_list():
            pg.draw.line(self.display, COLOR_LINE, world2screen((x1, y1)), world2screen((x2, y2)), 1)
            # pg.draw.line(self.display, COLOR_LINE, world2screen((x1, -y1 + 29)), world2screen((x2, -y2 + 29)), 1)
        # draw the path
        # convert to screen coordinates with world2screen(tuple)
        path = [world2screen(p) for p in test_path]
        if len(path) > 1:
            pg.draw.lines(self.display, pg.Color("red"), False, path, 2)

        # draw the particle filter positions
        for point in particle_filter.get_points():
            pg.draw.circle(self.display, (255, 0, 0), world2screen(point[0]), 2)
        self.display.blit(pg.transform.flip(self.display, False, True), (0, 0))
        pg.display.update()