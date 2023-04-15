from pacbot_arduino_manager import PacbotArduinoManager
from pacbot_comms import AutoRoboClient
from definitions import *

import pacbot_rs

from robot import Robot, DIST_BETWEEN_WHEELS
from bot_math import *
from grid import *
from path_tracker import PathTracker

from messages import *

import threading
import os
import pygame as pg

client_thread: threading.Thread | None = None
client: AutoRoboClient | None = None

pacbot_arduino_manager: PacbotArduinoManager | None = None

ADDRESS = os.environ.get("ADDRESS", 'localhost')
PORT = os.environ.get("PORT", 11297)

FPS = 100

USE_PROJECTOR = False
USE_REAL_ARDUINO = False

robot: Robot = Robot()
path_tracker: PathTracker = PathTracker()


def start_client():
    global client
    client = AutoRoboClient(ADDRESS, PORT, 10, tick_light=tick_relay_pacbot_position)
    client.run()


def tick_relay_pacbot_position(light_state: MsgType.LIGHT_STATE):
    """
    This method is called every tick.
    """
    if client is not None and not USE_PROJECTOR:
        client.update_fake_location((1, 1))


def get_cell_heuristic_value(pos: Position):
    return 0


def movement_loop():
    # determine position
    if USE_REAL_ARDUINO:
        # update the robot with encoder data
        arduino_data: IncomingArduinoMessage = pacbot_arduino_manager.get_sensor_data()

        left_encoder = arduino_data.encoder_values[0]  # the distance the left wheel has traveled forwards
        right_encoder = arduino_data.encoder_values[1]  # the distance the right wheel has traveled forwards

        dist_between_wheels = DIST_BETWEEN_WHEELS

        current_angle = robot.pose.angle

        # Calculate the change in position (x, y) and angle
        # Calculate the average distance traveled by both wheels
        average_distance = (left_encoder + right_encoder) / 2

        # Calculate the change in angle
        delta_angle = (right_encoder - left_encoder) / dist_between_wheels

        # Update the current angle with the change in angle
        new_angle = current_angle + delta_angle

        # Calculate the changes in x and y position using trigonometry
        delta_x = average_distance * math.cos(new_angle)
        delta_y = average_distance * math.sin(new_angle)

        # robot.pose = particle_filter(Pose(Position(delta_x, delta_y), delta_angle), arduino_data.ir_sensor_values)
        particle_filter_result = pf.update(average_distance, delta_angle, arduino_data.ir_sensor_values)
        robot.pose = Pose(Position(particle_filter_result[0][0], particle_filter_result[0][1]), particle_filter_result[1])
    else:
        # use the position from the robot which was updated when it moved
        pass

    # use the rounded position to determine the best high-level strategy move
    robot_int_position = Position(round(robot.pose.pos.x), round(robot.pose.pos.y))

    # # list of the 4 surrounding squares
    # surrounding_squares = [Position(robot_int_position.x + 1, robot_int_position.y),
    #                        Position(robot_int_position.x - 1, robot_int_position.y),
    #                        Position(robot_int_position.x, robot_int_position.y + 1),
    #                        Position(robot_int_position.x, robot_int_position.y - 1)]
    #
    # # find the best one
    # best_square = surrounding_squares[0]
    # best_square_heuristic = get_cell_heuristic_value(surrounding_squares[0])
    # for square in surrounding_squares:
    #     heuristic = get_cell_heuristic_value(square)
    #     if heuristic > best_square_heuristic:
    #         best_square_heuristic = heuristic
    #         best_square = square
    px = robot_int_position.x
    py = robot_int_position.y
    positions = [
        (px, py),
        (px, py + 1),
        (px, py - 1),
        (px - 1, py),
        (px + 1, py),
    ]

    values, action = pacbot_rs.get_action_heuristic_values(client.full_state)
    best_square = Position(*positions[action])

    # pathfind to it
    path = [best_square]
    if best_square != robot_int_position:
        path = grid_bfs_path(robot_int_position, best_square)

    # determine motor movements
    speed, angle = PathTracker.pure_pursuit(
        (robot.pose.pos.x, robot.pose.pos.y),
        robot.pose.angle,
        path,
        dt
    )

    # calculate speeds for left and right motors
    left_motor = speed - angle * DIST_BETWEEN_WHEELS / 2
    right_motor = speed + angle * DIST_BETWEEN_WHEELS / 2

    # execute motor movements
    if USE_REAL_ARDUINO:
        pacbot_arduino_manager.write_motors(left_motor, right_motor)
    else:
        robot.step(left_motor, right_motor, dt)
        client.update_fake_location((int(robot_int_position.x), int(robot_int_position.y)))


if __name__ == '__main__':
    # start the client thread
    client_thread = threading.Thread(target=start_client)
    client_thread.start()

    if USE_REAL_ARDUINO:
        # start the arduino manager
        manager = PacbotArduinoManager()

    # particle_filter_setup(robot.pose)
    pf = pacbot_rs.ParticleFilter((14, 7, 0))

    clock = pg.time.Clock()
    while 1:
        dt = clock.tick(FPS) / 1000
        if client.light_state.mode == client.light_state.PAUSED:
            pacbot_arduino_manager.write_motors(0, 0)
        else:
            movement_loop()
