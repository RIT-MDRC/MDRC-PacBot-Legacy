from bot_math import *
from PID_controller import *

# path tracker class that implements pure pursuit
class PathTracker:
    
    def __init__(self) -> None:
        self.turn_mode = False # when in turn mode, the robot will turn to face the next point in the path, otherwise pure pursuit
        self.PURE_PURSUIT_LOOKAHEAD = 1.5 # grid units
        self.TURN_MODE_CUTOFF = .02 # radians
        self.END_OF_PATH_CUTOFF = .05 # grid units
        self.previous_correction = 0
        
        self.previous_direction = 0
        
        self.heading_controller = PID_controller(2, 0, 0)
        self.drive_controller = PID_controller(1.5, 0, 0)

    def pure_pursuit(self, pos: tuple[float, float], angle: float, path: list[tuple[int, int]], dt: float) \
            -> tuple[float, float]:
        """
        Follow a path with the pure pursuit algorithm using current position, direction, path to follow, and grid state.
        Utilizes localization via particle filter and acceleration control via PID controller / trapezoid function.

        @param pos: The current position of the robot.
        @param angle: The current direction of the robot.
        @param path: The path to follow.
        @param dt: The time since the last frame

        @return: (speed, angle)  The speed and angle of the robot.
        """
        
        if len(path) < 2:
            return (0, 0)
        
        # normalize angle
        angle = normalize_angle(angle)
        
        # grab first line segment
        first_point = path[0]
        second_point = path[1]
        
        # work out if this line is vertical or horizontal
        if first_point[0] == second_point[0]: # vertical
            # work out where on the line the robot is
            robot_pos_projection = (first_point[0], pos[1])
            # work out look ahead position
            if first_point[1] < second_point[1]: # up
                if angle < -math.pi/2:
                    angle += 2*math.pi
                
                look_ahead_pos = (robot_pos_projection[0], robot_pos_projection[1] + self.PURE_PURSUIT_LOOKAHEAD)
                look_ahead_to_robot_angle = math.atan2(pos[0] - look_ahead_pos[0],
                                                    look_ahead_pos[1] - pos[1])
                correction_angle = -(look_ahead_to_robot_angle + ((math.pi/2)-angle))
                
                # check if we are at the end of the line
                if abs(pos[1]-second_point[1]) < self.END_OF_PATH_CUTOFF:
                    # remove the first line segment
                    path.pop(0)
                    self.previous_direction = 0
                
            else: # down
                if angle > math.pi/2:
                    angle -= 2*math.pi
                    
                
                look_ahead_pos = (robot_pos_projection[0], robot_pos_projection[1] - self.PURE_PURSUIT_LOOKAHEAD)
                look_ahead_to_robot_angle = math.atan2(pos[0] - look_ahead_pos[0],
                                                    pos[1] - look_ahead_pos[1])
                correction_angle = (look_ahead_to_robot_angle + ((math.pi/2)+angle))
                
                # check if we are at the end of the line
                if abs(pos[1] - second_point[1]) < self.END_OF_PATH_CUTOFF:
                    # remove the first line segment
                    path.pop(0)
                    self.previous_direction = 1
                    
        else: # horizontal
            # work out where on the line the robot is
            robot_pos_projection = (pos[0], first_point[1])
            # work out look ahead position
            if first_point[0] < second_point[0]: # right
                look_ahead_pos = (robot_pos_projection[0] + self.PURE_PURSUIT_LOOKAHEAD, robot_pos_projection[1])
                look_ahead_to_robot_angle = math.atan2(pos[1] - look_ahead_pos[1],
                                                    look_ahead_pos[0] - pos[0])
                correction_angle = (look_ahead_to_robot_angle + angle)
                
                # check if we are at the end of the line
                if abs(pos[0] - second_point[0]) < self.END_OF_PATH_CUTOFF:
                    # remove the first line segment
                    path.pop(0)
                    self.previous_direction = 2
                
            else: # left
                look_ahead_pos = (robot_pos_projection[0] - self.PURE_PURSUIT_LOOKAHEAD, robot_pos_projection[1])
                look_ahead_to_robot_angle = math.atan2(pos[1] - look_ahead_pos[1],
                                                    pos[0] - look_ahead_pos[0])
                
                # edge case
                if angle > 0:
                    correction_angle = -(look_ahead_to_robot_angle + ((math.pi)-angle))
                else:
                    correction_angle = -(look_ahead_to_robot_angle + (-(math.pi)-angle))
                    
                # check if we are at the end of the line
                if abs(pos[0] - second_point[0]) < self.END_OF_PATH_CUTOFF:
                    # remove the first line segment
                    path.pop(0)
                    self.previous_direction = 3
                
        # TODO: slow down when approaching the end of the line, and speed up at the start
        # calculate drive speed as a function of distance to the second point
        dist_to_look_ahead = math.sqrt((second_point[0] - pos[0])**2 + (second_point[1] - pos[1])**2)
        drive_speed = min(self.drive_controller.update(dist_to_look_ahead, dt), 1)
        
        if abs(self.previous_correction - correction_angle) > (math.pi/4):
            self.turn_mode = True
            
        if self.turn_mode:
            if abs(correction_angle) < self.TURN_MODE_CUTOFF:
                self.turn_mode = False
            drive_speed = 0
        
        self.previous_correction = correction_angle
                
        return (drive_speed, self.heading_controller.update(correction_angle, dt))