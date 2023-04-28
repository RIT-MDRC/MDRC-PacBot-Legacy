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

# DEBUG_VIS; if true, the robot will display a visualization of the particle filter and other info
DEBUG_VIS = os.environ.get("DEBUG_VIS", 'f') == 't'
# DEBUG_JSON; if true, the robot will save game info to json
DEBUG_JSON = os.environ.get("DEBUG_JSON", 'f') == 't'
# DEBUG_GAME_STATE; if true, the robot will include game state in json
DEBUG_GAME_STATE = os.environ.get("DEBUG_GAME_STATE", 'f') == 't'
# DEBUG_PF_INFO; if true, the robot will include the particle filter info in json
DEBUG_PF_INFO = os.environ.get("DEBUG_PF_INFO", 'f') == 't'

# USE_PROJECTOR; if false, the robot will manually send its location to the server
USE_PROJECTOR = os.environ.get("USE_PROJECTOR", 'f') == 't'
# USE_REAL_ARDUINO; if true, use the particle filter and arduino motors
USE_REAL_ARDUINO = os.environ.get("USE_REAL_ARDUINO", 'f') == 't'

# ADDRESS and PORT of the server
ADDRESS = os.environ.get("ADDRESS", 'localhost')
PORT = os.environ.get("PORT", 11297)

# Movement loop rate
FPS = 100

client_thread: threading.Thread | None = None
client: AutoRoboClient | None = None

pacbot_arduino_manager: PacbotArduinoManager | None = None
pure_pursuit = PathTracker()

# The current best guess robot position
robot: Robot = Robot()

# The global particle filter
# pf = pacbot_rs.ParticleFilter(14, 7, 0)
pf: pacbot_rs.ParticleFilter = pacbot_rs.ParticleFilter(9, 29, math.pi)

# The simulated visualization
sim_canvas: SimCanvas | None = None

# The debug information for each frame
debug_frames: list[DebugFrame] = []


def start_client_and_visualization_canvas():
    """
    Starts the client thread.
    @return:
    """
    global client, robot, pf, sim_canvas

    # Create a new event loop for this thread
    loop = asyncio.new_event_loop()

    # Set the new event loop as the default for this thread
    asyncio.set_event_loop(loop)

    # Create the client
    client = AutoRoboClient(ADDRESS, PORT, pf, 10, tick_light=tick_relay_pacbot_position)
    # Get the rust bot location, representing the start location
    robot.pose = Pose(
        Position(pf.get_pose()[0][0], pf.get_pose()[0][1]),
        pf.get_pose()[1]
    )
    # Set the location to the default Rust location
    client.update_fake_location((round(robot.pose.pos.x), round(robot.pose.pos.y)))

    if DEBUG_VIS:
        # Start the simulated visualization
        sim_canvas = SimCanvas(client.game_state, pf)
        sim_canvas.update(client.game_state, pf, robot, (robot.pose.pos.x, robot.pose.pos.y), [],
                          [0, 0, 0, 0, 0, 0, 0, 0])

    # Run the client indefinitely
    client.run()


def tick_relay_pacbot_position(_: MsgType.LIGHT_STATE):
    """
    This method is called every tick.
    """
    if client is not None and not USE_PROJECTOR:
        client.update_fake_location((robot.pose.pos.x, robot.pose.pos.y))


def movement_loop():
    global sim_canvas, debug_frames

    # debug info, set later
    arduino_data: IncomingArduinoMessage | None = None

    # determine position
    if USE_REAL_ARDUINO:
        # update the robot with encoder data
        arduino_data = pacbot_arduino_manager.get_sensor_data()

        # the distance the left wheel has traveled forwards
        left_encoder = arduino_data.encoder_values[0]
        # the distance the right wheel has traveled forwards
        right_encoder = arduino_data.encoder_values[1]

        dist_between_wheels = DIST_BETWEEN_WHEELS

        # Calculate the average distance traveled by both wheels
        average_distance = (left_encoder + right_encoder) / 2

        # Calculate the change in angle
        delta_angle = (right_encoder - left_encoder) / dist_between_wheels

        if USE_PROJECTOR:
            pf.rcv_position(client.full_state.pacman.x, client.full_state.pacman.y)
        particle_filter_result = pf.update(average_distance, delta_angle, list(arduino_data.ir_sensor_values))
        robot.pose = Pose(Position(particle_filter_result[0][0], particle_filter_result[0][1]),
                          particle_filter_result[1])
    else:
        # use the position from the robot which was updated when it moved
        pf.set_pose(robot.pose.pos.x, robot.pose.pos.y, robot.pose.angle)

    path = pacbot_rs.get_heuristic_path(client.game_state, 10)
    if len(path) >= 2:
        # determine whether the first segment is horizontal or vertical
        if path[0][0] == path[1][0]:
            # vertical
            # if pacbot is horizontally off by more than 0.1 grid cells, add the cell in that direction to the path
            if abs(robot.pose.pos.x - path[0][0]) > 0.1:
                path.insert(0, (
                    round(robot.pose.pos.x) + (-1 if robot.pose.pos.x < path[0][0] else 1), round(robot.pose.pos.y)))
        else:
            # horizontal
            # if pacbot is vertically off by more than 0.1 grid cells, add its current location to the path
            if abs(robot.pose.pos.y - path[0][1]) > 0.1:
                path.insert(0, (
                    round(robot.pose.pos.x), round(robot.pose.pos.y + (-1 if robot.pose.pos.y < path[0][1] else 1))))

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

    # update the server's knowledge of Pacbot's location
    if not USE_PROJECTOR:
        client.update_fake_location((round(robot.pose.pos.x), round(robot.pose.pos.y)))

    if sim_canvas is not None:
        sim_canvas.update(client.game_state, pf, robot, path[0], [Position(x1, y1) for (x1, y1) in path],
                          pacbot_arduino_manager.latest_message.ir_sensor_values if USE_REAL_ARDUINO else [0, 0, 0, 0,
                                                                                                           0])

    arduino_lines_read, arduino_lines_sent = pacbot_arduino_manager.get_debug_lines() if USE_REAL_ARDUINO else ([], [])

    if DEBUG_JSON:
        debug_frame = DebugFrame(
            USE_REAL_ARDUINO=USE_REAL_ARDUINO,
            USE_PROJECTOR=USE_PROJECTOR,
            ADDRESS=ADDRESS,
            PORT=PORT,

            game_state=client.full_state.SerializeToString() if DEBUG_GAME_STATE else None,

            pacbot_pose=robot.pose,
            pacbot_pose_sensor_readings=pf.get_sense_distances(),

            pf_points=pf.get_points() if DEBUG_PF_INFO else [],
            pf_map_segments=pf.get_map_segments_list() if DEBUG_PF_INFO else [],
            pf_empty_grid_cells=pf.get_empty_grid_cells() if DEBUG_PF_INFO else [],

            target_pos=Position(path[0][0], path[0][1]),
            target_path=[Position(x1, y1) for (x1, y1) in path],

            pp_speed=speed,
            pp_angle=angle,
            pp_left_motor=left_motor,
            pp_right_motor=right_motor,

            encoder_readings=arduino_data.encoder_values if arduino_data is not None else [0, 0],
            ir_sensor_readings=arduino_data.ir_sensor_values if arduino_data is not None else [0, 0, 0, 0, 0],

            lines_read=arduino_lines_read if USE_REAL_ARDUINO else None,
            lines_sent=arduino_lines_sent if USE_REAL_ARDUINO else None,
        )

        debug_frames.append(json.loads(json.dumps(debug_frame)))

        with open('debug.json', 'w') as f:
            f.write(json.dumps(debug_frames))


if __name__ == '__main__':
    # start the client thread
    client_thread = threading.Thread(target=start_client_and_visualization_canvas)
    client_thread.start()

    if USE_REAL_ARDUINO:
        # start the arduino manager
        pacbot_arduino_manager = PacbotArduinoManager()

    clock = pg.time.Clock()
    while 1:
        dt = clock.tick(FPS) / 1000
        if client is None or client.light_state is None or client.full_state is None:
            # client has not yet received any game state from the server
            continue
        if client.light_state.mode == client.light_state.PAUSED:
            # if paused, turn off motors
            if USE_REAL_ARDUINO:
                pacbot_arduino_manager.write_motors(0, 0)
        else:
            movement_loop()
