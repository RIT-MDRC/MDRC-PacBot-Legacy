from bot_math import Pose, Position
import pacbot_rs
import pygame as pg
from grid import GRID_WIDTH, GRID_HEIGHT, GRID
import math

DRAW_SCALE = 30

SCREENRECT = pg.Rect(
    0, 0, (GRID_WIDTH + 2) * DRAW_SCALE, (GRID_HEIGHT + 2) * DRAW_SCALE
)
COLOR_BG_WHITE = (255, 255, 255)
COLOR_LINE_BLACK = (0, 0, 0)
COLOR_WALL_FILL_GREY = (192, 192, 192)
COLOR_ROBOT_BLUE = (0, 0, 255)
COLOR_SIMULATED_RAYCAST_RED = (255, 0, 0)
COLOR_SENSOR_DISTANCE_GREEN = (0, 200, 0)
COLOR_POINT_YELLOW = (255, 255, 0)
COLOR_TEXT_BLACK = (0, 0, 0)

FPS = 60

ROBOT_RADIUS_GRID_UNITS = (6 / 3.5) / 2
ROBOT_RADIUS = DRAW_SCALE * ROBOT_RADIUS_GRID_UNITS
SENSOR_ANGLES = [math.pi / 2, math.pi / 4, 0, -math.pi / 4, -math.pi / 2]
SENSOR_DISTANCE_FROM_CENTER = 2 * 0.75 / 2.0  # a passage is 2 grid units wide


def world2screen(world_pos: tuple[float, float]) -> tuple[float, float]:
    """Convert world coordinates to screen coordinates."""
    wx, wy = world_pos
    return (wx + 1) * DRAW_SCALE, (wy + 1) * DRAW_SCALE


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
        pg.font.init()

        win_style = 0  # |FULLSCREEN

        best_depth = pg.display.mode_ok(SCREENRECT.size, win_style, 32)
        self.display = pg.display.set_mode(SCREENRECT.size, win_style, best_depth)

        self.background_image = pg.Surface(SCREENRECT.size).convert()
        self.bg_rect = self.background_image.get_rect(
            center=(SCREENRECT.width // 2, SCREENRECT.height // 2)
        )

        # fill the background color
        pg.draw.rect(self.background_image, COLOR_BG_WHITE, self.bg_rect)

        # fill the walls
        alt_grid = get_alt_grid()
        for x in range(GRID_WIDTH + 1):
            for y in range(GRID_HEIGHT + 1):
                if alt_grid[x][y]:
                    rect = pg.Rect(*world2screen((x - 1, GRID_HEIGHT - y - 1)), DRAW_SCALE, DRAW_SCALE)
                    pg.draw.rect(self.background_image, COLOR_WALL_FILL_GREY, rect)

        # draw edges
        rect = pg.Rect(*world2screen((-1, GRID_HEIGHT)), (GRID_WIDTH + 1) * DRAW_SCALE, DRAW_SCALE)
        pg.draw.rect(self.background_image, COLOR_WALL_FILL_GREY, rect)
        rect = pg.Rect(*world2screen((GRID_WIDTH, -1)), DRAW_SCALE, (GRID_HEIGHT + 2) * DRAW_SCALE)
        pg.draw.rect(self.background_image, COLOR_WALL_FILL_GREY, rect)

        pg.display.flip()

    def update(self, game_state: pacbot_rs.GameState, particle_filter: pacbot_rs.ParticleFilter, robot: Robot,
               destination: (int, int), test_path: list[Position], sensors: list[float]):
        self.game_state = game_state
        self.particle_filter = particle_filter

        # process quit event
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

        # draw the map segments
        for (x1, x2, y1, y2) in particle_filter.get_map_segments_list():
            pg.draw.line(self.display, COLOR_LINE_BLACK, world2screen((x1, y1)), world2screen((x2, y2)), 1)

        # draw the particle filter positions
        for point in particle_filter.get_points():
            pg.draw.circle(self.display, COLOR_POINT_YELLOW, world2screen(point[0]), 1)

        # draw the path
        path = [world2screen((p.x, p.y)) for p in test_path]
        if len(path) > 1:
            pg.draw.lines(self.display, COLOR_ROBOT_BLUE, False, path, 2)

        # draw the robot
        robot.draw(self.display)

        # pf_robot is the particle filter's idea of where the robot is
        pf_pose = particle_filter.get_pose()
        pf_robot = Robot()
        pf_robot.pose = Pose(
            Position(pf_pose[0][0], pf_pose[0][1]),
            pf_pose[1]
        )
        pf_robot.draw(self.display)

        # this dot represents the robot's destination
        pg.draw.circle(self.display, COLOR_SENSOR_DISTANCE_GREEN, world2screen((destination[0], destination[1])), 5)

        # draw the sensor distances, both simulated raycast and measured
        # print(sensors[:4])
        for i in range(5):
            if i == 4:
                continue  # sensor broken
            angle = SENSOR_ANGLES[i]

            for (color, distance) in [
                # draw line from pacbot to the simulated wall
                (COLOR_SIMULATED_RAYCAST_RED, particle_filter.get_sense_distances()[i])
                # draw a line representing the measured sensor distance
                # (COLOR_SENSOR_DISTANCE_GREEN, sensors[i] + SENSOR_DISTANCE_FROM_CENTER)
            ]:
                if distance - ROBOT_RADIUS_GRID_UNITS <= 0:
                    continue
                # draw the line
                pg.draw.line(self.display, color, world2screen((
                    # start of line
                    pf_pose[0][0] + ROBOT_RADIUS_GRID_UNITS * math.cos(pf_pose[1] + angle),
                    pf_pose[0][1] + ROBOT_RADIUS_GRID_UNITS * math.sin(pf_pose[1] + angle)
                )), world2screen((
                    # end of line
                    pf_pose[0][0] + distance * math.cos(pf_pose[1] + angle),
                    pf_pose[0][1] + distance * math.sin(pf_pose[1] + angle)
                )), 2)
                # draw the dot at the end of the line
                pg.draw.circle(self.display, color, world2screen((
                    pf_pose[0][0] + distance * math.cos(pf_pose[1] + angle),
                    pf_pose[0][1] + distance * math.sin(pf_pose[1] + angle)
                )), 3)

        # draw coordinate markers for y axis on screen; draw the numbers upside down
        font = pg.font.SysFont("Arial", 12)
        for y in range(GRID_HEIGHT + 1):
            text = font.render(str(y), True, COLOR_LINE_BLACK)
            text_rect = text.get_rect()
            text_rect.center = world2screen((-0.5, y))
            self.display.blit(pg.transform.flip(text, False, True), text_rect)

        # draw coordinate markers for x axis on screen
        for x in range(GRID_WIDTH + 1):
            text = font.render(str(x), True, COLOR_LINE_BLACK)
            text_rect = text.get_rect()
            text_rect.center = world2screen((x, -0.5))
            self.display.blit(pg.transform.flip(text, False, True), text_rect)

        # flip display to match orientation of other visualization
        self.display.blit(pg.transform.flip(self.display, False, True), (0, 0))
        # update display
        pg.display.update()
