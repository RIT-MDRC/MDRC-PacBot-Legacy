from grid import *
import math

PURE_PURSUIT_LOOKAHEAD = 0.5 # grid units


def high_level_strategy(pos: tuple[int, int], direction: int) -> tuple[int, int]:
    """
    Determines the target location based on the current position, direction, and grid state.

    @param pos: The current position of the robot.
    @param direction: The current direction of the robot.
    @param grid: The current shape of the grid.

    @return: The target location.
    """
    pass


def path_finding(pos: tuple[int, int], target: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Determines the path to the target location based on the current position, target location, and grid state.

    @param pos: The current position of the robot.
    @param target: The target location.
    @param grid: The current shape of the grid.

    @return: The path to the target location. Only includes endpoints of lines.
    """
    pass


def pure_pursuit(pos: tuple[float, float], angle: float, path: list[tuple[int, int]]) \
        -> tuple[float, float]:
    """
    Follow a path with the pure pursuit algorithm using current position, direction, path to follow, and grid state.
    Utilizes localization via particle filter and acceleration control via PID controller / trapezoid function.

    @param pos: The current position of the robot.
    @param angle: The current direction of the robot.
    @param path: The path to follow.
    @param grid: The current shape of the grid.

    @return: (speed, angle)  The speed and angle of the robot.
    """
    
    if len(path) < 2:
        return (0, 0)
    
    # grab first line segment
    first_point = path[0]
    second_point = path[1]
    
    # work out if this line is vertical or horizontal
    if first_point[0] == second_point[0]: # vertical
        # work out where on the line the robot is
        robot_pos_projection = (first_point[0], pos[1])
        # work out look ahead position
        if first_point[1] < second_point[1]: # up
            look_ahead_pos = (robot_pos_projection[0], robot_pos_projection[1] + PURE_PURSUIT_LOOKAHEAD)
            look_ahead_to_robot_angle = math.atan2(pos[0] - look_ahead_pos[0],
                                                   look_ahead_pos[1] - pos[1])
            correction_angle = (look_ahead_to_robot_angle + (90-angle))
            
            # check if we are at the end of the line
            if look_ahead_pos[1] > second_point[1]:
                # remove the first line segment
                path.pop(0)
            
        else: # down
            look_ahead_pos = (robot_pos_projection[0], robot_pos_projection[1] - PURE_PURSUIT_LOOKAHEAD)
            look_ahead_to_robot_angle = math.atan2(pos[0] - look_ahead_pos[0],
                                                   pos[1] - look_ahead_pos[1])
            correction_angle = -(look_ahead_to_robot_angle + (90+angle))
            
            # check if we are at the end of the line
            if look_ahead_pos[1] < second_point[1]:
                # remove the first line segment
                path.pop(0)
                
    else: # horizontal
        # work out where on the line the robot is
        robot_pos_projection = (pos[0], first_point[1])
        # work out look ahead position
        if first_point[0] < second_point[0]: # right
            look_ahead_pos = (robot_pos_projection[0] + PURE_PURSUIT_LOOKAHEAD, robot_pos_projection[1])
            look_ahead_to_robot_angle = math.atan2(pos[1] - look_ahead_pos[1],
                                                   look_ahead_pos[0] - pos[0])
            correction_angle = -(look_ahead_to_robot_angle + angle)
            
            # check if we are at the end of the line
            if look_ahead_pos[0] > second_point[0]:
                # remove the first line segment
                path.pop(0)
            
        else: # left
            look_ahead_pos = (robot_pos_projection[0] - PURE_PURSUIT_LOOKAHEAD, robot_pos_projection[1])
            look_ahead_to_robot_angle = math.atan2(pos[1] - look_ahead_pos[1],
                                                   pos[0] - look_ahead_pos[0])
            # edge case
            if angle > 0:
                correction_angle = -(look_ahead_to_robot_angle + (180-angle))
            else:
                correction_angle = -(look_ahead_to_robot_angle + (-180-angle))
                
            # check if we are at the end of the line
            if look_ahead_pos[0] < second_point[0]:
                # remove the first line segment
                path.pop(0)
            
    return (1, correction_angle)


def wheel_control(heading: tuple[float, float]):
    """
    Controls the wheels of the robot based on the desired speed and heading.

    @param heading: The heading of the robot; the magnitude of the values determines the speed, the ratio determines the angle.
    """
    pass
