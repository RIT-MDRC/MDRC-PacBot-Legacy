from grid import *
import math

from bot_math import Pose, Position
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
    bfs_nodes: list[tuple[int, Pose]] = [(-1, pose)]
    # represent the index where all indices <= this index were added in the last iteration
    last_added_indices = 0

    while 1:
        new_last_added_indices = len(bfs_nodes)
        # add new nodes to list
        for pose_change in [
                [1, 0, 0],
                [-1, 0, 0],
                [0, 1, 0],
                [0, -1, 0],
                [0, 0, math.pi/2],
                [0, 0, math.pi],
                [0, 0, 3*math.pi/2],
            ]:
            for pose_i in range(last_added_indices, len(bfs_nodes)):
                prev_i, pose = bfs_nodes[pose_i]
                new_pose = Pose(Position(pose.pos.x + pose_change[0], pose.pos.y + pose_change[1]), pose.angle + pose_change[2])
                if new_pose.pos not in get_grid_open_spaces():
                    continue
                if new_pose.pos == target:
                    # success, return path
                    path = [new_pose]
                    while prev_i > 0:
                        path = [bfs_nodes[prev_i][1]] + path
                        prev_i = bfs_nodes[prev_i][0]
                    return path
                already_found = False
                for prev_i, bfs_pose in bfs_nodes:
                    if bfs_pose == new_pose:
                        already_found = True
                        break
                if not already_found:
                    bfs_nodes.append((pose_i, new_pose))
        if new_last_added_indices == len(bfs_nodes):
            return []
        last_added_indices = new_last_added_indices


def wheel_control(heading: tuple[float, float]):
    """
    Controls the wheels of the robot based on the desired speed and heading.

    @param heading: The heading of the robot; the magnitude of the values determines the speed, the ratio determines the angle.
    """
    pass
