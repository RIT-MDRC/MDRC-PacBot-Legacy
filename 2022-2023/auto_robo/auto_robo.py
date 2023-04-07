# @author Michael Elia
# @date 2023-04-06

import os
import subprocess
import sys
import threading
import robomodules as rm
import argparse as ap

from Pacbot.src.gameEngine.messages import *

from typing import Callable


class AutoRobo:
    """
    This class facilitates running and communication with the services provided by the HarvardURC_Pacbot repo.

    It uses robomodules, a custom library for communicating with the Harvard Robotics Club's server.
    """

    ADDRESS = 'localhost'
    PORT = 11297

    GAME_ENGINE_PATH = os.path.join('Pacbot', 'src', 'gameEngine')
    LOGS_PATH = None

    processes = {
        'server': {
            'file': 'server.py',
            'running': False,
            'process': None
        },
        'gameEngine': {
            'file': 'gameEngine.py',
            'running': False,
            'process': None
        },
        'visualize': {
            'file': 'visualize.py',
            'running': False,
            'process': None
        },
        'terminalPrinter': {
            'file': 'terminalPrinter.py',
            'running': False,
            'process': None
        },
        'keyboardInput': {
            'file': 'keyboardInput.py',
            'running': False,
            'process': None
        }
    }

    def __init__(self, addr, port, game_engine_path=None, logs_path=None):
        """
        Builds a new AutoRobo object.
        @param addr: The address of the server
        @param port: The port of the server
        """
        self.ADDRESS = addr
        self.PORT = port

        if game_engine_path is not None:
            self.GAME_ENGINE_PATH = game_engine_path

        if logs_path is not None:
            self.LOGS_PATH = logs_path

        self.start_process('server')

    def start_process(self, process_name):
        """
        Starts a process.
        """
        if self.processes[process_name]['running']:
            return

        env = os.environ.copy()
        env.update({'BIND_ADDRESS': self.ADDRESS, 'BIND_PORT': str(self.PORT)})

        self.processes[process_name]['running'] = True
        if self.LOGS_PATH is not None:
            with open(os.path.join(self.LOGS_PATH, f'{process_name}_stdout.log'), 'w') as f:
                with open(os.path.join(self.LOGS_PATH, f'{process_name}_stderr.log'), 'w') as g:
                    self.processes[process_name]['process'] = subprocess.Popen(
                        [sys.executable, os.path.join(self.GAME_ENGINE_PATH, self.processes[process_name]['file'])],
                        stdin=subprocess.PIPE,
                        stdout=f,
                        stderr=g,
                        text=True,
                        env=env)
        else:
            self.processes[process_name]['process'] = subprocess.Popen(
                [sys.executable, self.processes[process_name]['file']],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env={'BIND_ADDRESS': self.ADDRESS, 'BIND_PORT': str(self.PORT)})

        print(f'{process_name} started')

    def stop_process(self, process_name):
        """
        Stops a process.
        """
        if not self.processes[process_name]['running']:
            return

        # don't allow other processes to run without the server
        if process_name == 'server':
            for proc in self.processes:
                if proc != 'server':
                    self.stop_process(proc)

        self.processes[process_name]['process'].terminate()
        self.processes[process_name]['process'] = None
        self.processes[process_name]['running'] = False

        print(f'{process_name} stopped')

        if process_name == 'server':
            exit()


class AutoRoboClient(rm.ProtoModule):
    """
    This class acts as a client to the AutoRobo class.
    """

    ADDRESS = 'localhost'
    PORT = 11297

    # times per second that tick() and custom_tick() are called
    FREQUENCY = 10
    custom_tick: Callable[[MsgType.LIGHT_STATE], None] = None

    state: MsgType.LIGHT_STATE = None

    # The location of the pacman in the maze, as given by the bot code when in simulation
    pacman_fake_location: tuple[2] = (1, 1)

    def __init__(self, addr, port, freq=10, tick: Callable[[MsgType.LIGHT_STATE], None] = None):
        """
        Builds a new AutoRoboClient object.
        @param addr: The address of the server
        @param port: The port of the server
        @param freq: The optional frequency (per second) that custom_tick() is called
        @param tick: The optional custom tick function, called every 1/freq seconds
        """
        self.ADDRESS = addr
        self.PORT = port
        self.FREQUENCY = freq
        self.custom_tick = tick

        self.subscriptions = [MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, self.FREQUENCY, self.subscriptions)
        self.state = None

    def msg_received(self, msg, msg_type):
        """
        This method is called whenever a message is received from the server.
        """
        if msg_type == MsgType.LIGHT_STATE:
            self.state = msg

    def tick(self):
        """
        This method is called every tick.
        """
        if self.custom_tick is not None and self.state is not None:
            self.custom_tick(self.state)

    def update_fake_location(self, location: tuple[2]):
        """
        This method can be called by the bot code to update Pacbot's location
        """
        self.pacman_fake_location = location

        new_msg = PacmanState.AgentState()
        # Required X and Y location
        new_msg.x = self.pacman_fake_location[0]
        new_msg.y = self.pacman_fake_location[1]

        self.write(new_msg.SerializeToString(), MsgType.PACMAN_LOCATION)


if __name__ == "__main__":
    # Parse arguments
    parser = ap.ArgumentParser()

    parser.add_argument('--address', '-a', type=str, default='localhost', help='The address of the server')
    parser.add_argument('--port', '-p', type=int, default=11297, help='The port of the server')

    parser.add_argument('--game-engine-path', '-g', type=str, default=None, help='The path to the game engine folder')
    parser.add_argument('--logs-path', '-l', type=str, default=None, help='The path to the logs folder')

    args = parser.parse_args()

    # Create the server
    server = AutoRobo(args.address, args.port, args.game_engine_path, args.logs_path)

    # User menu
    while True:
        print('''
0) Stop Server
1) Start Game Engine
2) Stop Game Engine
3) Start Visualization
4) Stop Visualization
5) Start Terminal Printer
6) Start Keyboard Input
''')

        choice = input('Enter your choice: ')

        match choice:
            case '0':
                server.stop_process('server')
            case '1':
                server.start_process('gameEngine')
            case '2':
                server.stop_process('gameEngine')
            case '3':
                server.start_process('visualize')
            case '4':
                server.stop_process('visualize')
            case '5':
                server.start_process('terminalPrinter')
            case '6':
                server.start_process('keyboardInput')
            case _:
                print('Invalid choice')
