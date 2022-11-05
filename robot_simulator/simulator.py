import pygame as pg
import random
import math
from typing import NamedTuple

from grid import *


class HorizontalSegment(NamedTuple):
    x_start: int
    x_end: int
    y: int


class VerticalSegment(NamedTuple):
    y_start: int
    y_end: int
    x: int


def get_alt_grid():
    alt_grid = [[True] * (GRID_HEIGHT + 1) for _ in range(GRID_WIDTH + 1)]
    for x in range(GRID_WIDTH - 1):
        for y in range(GRID_HEIGHT - 1):
            alt_grid[x + 1][y + 1] = (
                GRID[x][y] and GRID[x + 1][y] and GRID[x][y + 1] and GRID[x + 1][y + 1]
            )
    return alt_grid


GRID = get_alt_grid()
GRID_WIDTH = len(GRID)
GRID_HEIGHT = len(GRID[0])


def get_map_segments(grid) -> list[HorizontalSegment]:
    """Returns the X and Y line segments in the map."""
    grid_width = len(grid)
    grid_height = len(grid[0])

    x_segments = []
    for y in range(0, grid_height - 1):
        seg_start_x = None
        for x in range(0, grid_width):
            is_wall_here = grid[x][y] != grid[x][y + 1]
            if is_wall_here and seg_start_x is None:
                seg_start_x = x
            if not is_wall_here and seg_start_x is not None:
                x_segments.append(HorizontalSegment(seg_start_x, x, y + 1))
                seg_start_x = None

    y_segments = []
    for x in range(0, grid_width - 1):
        seg_start_y = None
        for y in range(0, grid_height):
            is_wall_here = grid[x][y] != grid[x + 1][y]
            if is_wall_here and seg_start_y is None:
                seg_start_y = y
            if not is_wall_here and seg_start_y is not None:
                y_segments.append(VerticalSegment(seg_start_y, y, x + 1))
                seg_start_y = None

    return x_segments, y_segments


x_segments, y_segments = get_map_segments(GRID)


DRAW_SCALE = 30


def world2screen(world_pos: tuple[float, float]) -> tuple[float, float]:
    """Convert world coordinates to screen coordinates."""
    wx, wy = world_pos
    return ((wx + 1) * DRAW_SCALE, (wy + 1) * DRAW_SCALE)


SCREENRECT = pg.Rect(
    0, 0, (GRID_WIDTH + 2) * DRAW_SCALE, (GRID_HEIGHT + 2) * DRAW_SCALE
)
COLOR_BG = (255, 255, 255)
COLOR_LINE = (0, 0, 0)
COLOR_WALL_FILL = (192, 192, 192)
COLOR_ROBOT = (0, 0, 255)


class Robot:
    def __init__(self):
        self.x = 14.5
        self.y = 18.0
        self.angle = 0.0  # radians

    def draw(self, surface):
        center = world2screen((self.x, self.y))
        radius = DRAW_SCALE * (6 / 3.5) / 2
        pg.draw.circle(surface, COLOR_ROBOT, center, radius, width=2)
        end_pos = (
            center[0] + math.cos(self.angle) * radius,
            center[1] + math.sin(self.angle) * radius,
        )
        pg.draw.line(surface, COLOR_ROBOT, center, end_pos)


def raycast(start_pos: tuple[float, float], angle: float) -> float:
    ...  # TODO


def main():
    pg.init()

    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    display = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    background_image = pg.Surface(SCREENRECT.size).convert()
    bg_rect = background_image.get_rect(
        center=(SCREENRECT.width // 2, SCREENRECT.height // 2)
    )

    # fill the background color
    pg.draw.rect(background_image, COLOR_BG, bg_rect)

    # fill the walls
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if GRID[x][y]:
                rect = pg.Rect(*world2screen((x, y)), DRAW_SCALE, DRAW_SCALE)
                pg.draw.rect(background_image, COLOR_WALL_FILL, rect)

    # draw all the line segments
    for x_seg in x_segments:
        start_pos = world2screen((x_seg.x_start, x_seg.y))
        end_pos = world2screen((x_seg.x_end, x_seg.y))
        pg.draw.line(background_image, COLOR_LINE, start_pos, end_pos)
    for y_seg in y_segments:
        start_pos = world2screen((y_seg.x, y_seg.y_start))
        end_pos = world2screen((y_seg.x, y_seg.y_end))
        pg.draw.line(background_image, COLOR_LINE, start_pos, end_pos)

    pg.display.flip()

    robot = Robot()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                elif event.key == pg.K_f:
                    pass  # ...

        # clear / draw the background
        display.blit(background_image, bg_rect)

        # draw the robot
        robot.draw(display)

        pg.display.update()


if __name__ == "__main__":
    main()
    pg.quit()
