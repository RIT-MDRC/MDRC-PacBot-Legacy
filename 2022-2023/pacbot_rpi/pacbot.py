from pacbot_arduino_manager import PacbotArduinoManager
from pacbot_comms import AutoRoboClient
from definitions import *
import asyncio
import json
import pacbot_rs

from robot import Robot, DIST_BETWEEN_WHEELS
from bot_math import *
from grid import *
from path_tracker import PathTracker
from sim_canvas import SimCanvas

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

USE_PROJECTOR = os.environ.get("USE_PROJECTOR", 'f') == 't'
USE_REAL_ARDUINO = os.environ.get("USE_REAL_ARDUINO", 'f') == 't'

robot: Robot = Robot()
path_tracker: PathTracker = PathTracker()


def start_client():
    global client, pf, sim_canvas

    # Create a new event loop for this thread
    loop = asyncio.new_event_loop()

    # Set the new event loop as the default for this thread
    asyncio.set_event_loop(loop)

    client = AutoRoboClient(ADDRESS, PORT, pf, 10, tick_light=tick_relay_pacbot_position)
    client.update_fake_location((robot.pose.pos.x, robot.pose.pos.y))

    client.run()


def tick_relay_pacbot_position(light_state: MsgType.LIGHT_STATE):
    """
    This method is called every tick.
    """
    if client is not None and not USE_PROJECTOR:
        # print('ticking pacman location ' + str(robot.pose))
        # client.update_fake_location((robot.pose.pos.x, robot.pose.pos.y // 2 - 1))
        client.update_fake_location((robot.pose.pos.x, robot.pose.pos.y))


def get_cell_heuristic_value(pos: Position):
    return 0

pointspf = []

prev_best_square = None
def movement_loop():
    global sim_canvas, prev_best_square, pointspf
    #print('MOVEMENT LOOP')
    # determine position
    if USE_REAL_ARDUINO:
        # update the robot with encoder data
        #print('READ')
        arduino_data: IncomingArduinoMessage = pacbot_arduino_manager.get_sensor_data()
        #print('AFTER READ')

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
        #print('DOING UPDATE')
        particle_filter_result = pf.update(average_distance, delta_angle, list(arduino_data.ir_sensor_values))
        robot.pose = Pose(Position(particle_filter_result[0][0], particle_filter_result[0][1]), particle_filter_result[1])
    else:
        # use the position from the robot which was updated when it moved
        pass
    #print('AFTER UPDATE')
    #pointspf.append(pf.get_points())
    #pointspf = json.loads(json.dumps(pointspf))
    #print(pf.get_points()[0])
    #pf1 = pf.get_points()
    #pf2 = pf.get_points()
    #print(id(pf1))
    #print(id(pf2))
    with open('test.txt', 'w') as f:
        f.write(json.dumps(pointspf))

    # use the rounded position to determine the best high-level strategy move
    robot_int_position = Position(round(robot.pose.pos.x), round(robot.pose.pos.y))
    print(robot_int_position)
    px = robot_int_position.x
    py = robot_int_position.y
    positions = [
        (px, py),
        (px, py + 1),
        (px, py - 1),
        (px - 1, py),
        (px + 1, py),
    ]

    # values, action = pacbot_rs.get_action_heuristic_values(client.game_state)
    # best_square: list[int] = [int(positions[action][0]), int(positions[action][1])]

    path = pacbot_rs.get_heuristic_path(client.game_state, 10)
    # for i in range(3):
    #     client.game_state.pacbot.update((best_square[0], best_square[1]))
    #     values, action = pacbot_rs.get_action_heuristic_values(client.game_state)
    #     best_square = [int(positions[action][0]), int(positions[action][1])]
    # client.game_state.pacbot.update((int(px), int(py)))

    # if best_square != prev_best_square:
    #     print('best square changed to', best_square)
    #     prev_best_square = best_square
    #
    # # pathfind to it
    # path = grid_bfs_path(robot_int_position, Position(best_square[0], best_square[1]))
    # # path = [(int(best_square[0]), int(best_square[1]))]
    # if best_square != robot_int_position:
    #     # path = grid_bfs_path(robot_int_position, best_square)
    #     path = [(px, py), (int(best_square[0]), int(best_square[1]))]

    if sim_canvas is not None:
        sim_canvas.update(client.game_state, pf, robot, path[0], [Position(x1, y1) for (x1, y1) in path],
                          pacbot_arduino_manager.latest_message.ir_sensor_values)
    elif client is not None:
        sim_canvas = SimCanvas(client.game_state, pf)

    # determine motor movements
    (speed, angle) = pure_pursuit.pure_pursuit(
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
        # client.update_fake_location((round(robot_int_position.x), round(robot_int_position.y)))


if __name__ == '__main__':
    # particle_filter_setup(robot.pose)
    # pf = pacbot_rs.ParticleFilter(14, 7, 0)
    pf = pacbot_rs.ParticleFilter(4, 29, math.pi)

    sim_canvas: SimCanvas | None = None

    # start the client thread
    client_thread = threading.Thread(target=start_client)
    client_thread.start()

    if USE_REAL_ARDUINO:
        # start the arduino manager
        pacbot_arduino_manager = PacbotArduinoManager()

    pure_pursuit = PathTracker()

    clock = pg.time.Clock()
    while 1:
        dt = clock.tick(FPS) / 1000
        if client is None or client.light_state is None or client.full_state is None:
            continue
        if client.light_state.mode == client.light_state.PAUSED:
            if USE_REAL_ARDUINO:
                pacbot_arduino_manager.write_motors(0, 0)
        else:
            # print('movement loop')
            movement_loop()
