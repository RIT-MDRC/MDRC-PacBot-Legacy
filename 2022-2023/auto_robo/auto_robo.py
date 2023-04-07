# @author Michael Elia
# @date 2023-04-06

import os
import subprocess
import sys
import robomodules as rm
import argparse as ap
import tty
import termios
import pty
import json

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
        },
        'recorder': {
            'file': '',
            'running': False,
            'process': None
        },
        'playback': {
            'file': '',
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

        execute = [sys.executable, self.processes[process_name]['file']]

        working_path = self.GAME_ENGINE_PATH

        if process_name == 'recorder':
            record_file = input('Enter the name of the file to record to: ')

            execute[1] = os.path.basename(__file__)
            execute.append('-r')
            execute.append(record_file)

            working_path = os.getcwd()

        if process_name == 'playback':
            playback_file = input('Enter the name of the file to playback: ')

            execute[1] = os.path.basename(__file__)
            execute.append('-b')
            execute.append(playback_file)

            working_path = os.getcwd()

        if process_name == 'visualize':
            execute.append('-w')
            execute.append('-p')

        if process_name != 'keyboardInput':
            self.processes[process_name]['running'] = True
            if self.LOGS_PATH is not None:
                with open(os.path.join(self.LOGS_PATH, f'{process_name}_stdout.log'), 'w') as f:
                    with open(os.path.join(self.LOGS_PATH, f'{process_name}_stderr.log'), 'w') as g:
                        self.processes[process_name]['process'] = subprocess.Popen(
                            execute,
                            stdin=subprocess.PIPE,
                            stdout=f,
                            stderr=g,
                            text=True,
                            env=env,
                            cwd=working_path)
            else:
                self.processes[process_name]['process'] = subprocess.Popen(
                    execute,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=env,
                    cwd=working_path)

            print(f'{process_name} started')

        elif process_name == 'keyboardInput':
            print('Redirecting input to keyboardInput.py; press q to quit')

            # Create a pseudoterminal master and slave pair
            master_fd, slave_fd = pty.openpty()

            # Launch the external module with the slave pseudoterminal for communication
            process = subprocess.Popen(
                [sys.executable, self.processes[process_name]['file']],
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=subprocess.PIPE,
                env=env,
                cwd=self.GAME_ENGINE_PATH
            )

            try:
                while True:
                    # Get keypress from the user
                    key = self.get_key()

                    if key is None:
                        break

                    # Send the keypress to the external module via the master pseudoterminal
                    os.write(master_fd, key.encode())

                    # If the user pressed 'q', exit the loop
                    if key == 'q':
                        break

            finally:
                # Close the pseudoterminal file descriptors
                os.close(master_fd)
                os.close(slave_fd)

                # Terminate the process
                process.terminate()

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

    def get_key(self):
        try:
            old_settings = termios.tcgetattr(sys.stdin)
        except:
            print('Please only run keyboard input in a terminal.')
            return None
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        return ch

    def send_input(self, process_name, text):
        """
        Sends input to a process.
        """
        if not self.processes[process_name]['running']:
            return

        self.processes[process_name]['process'].stdin.write(text)
        self.processes[process_name]['process'].stdin.flush()


class AutoRoboRecorder(rm.ProtoModule):
    """
    This class provides functionality to record games
    """

    ADDRESS = 'localhost'
    PORT = 11297

    # times per second that tick() and custom_tick() are called
    FREQUENCY = 10

    states: list[MsgType.FULL_STATE] = []

    SAVE_FILE = None

    def __init__(self, addr, port, save_file):
        """
        Builds a new AutoRoboRecorder object.
        @param addr: The address of the server
        @param port: The port of the server
        """
        self.ADDRESS = addr
        self.PORT = port
        self.SAVE_FILE = save_file

        print('Recording game to ' + self.SAVE_FILE)

        self.subscriptions = [MsgType.FULL_STATE]
        super().__init__(addr, port, message_buffers, MsgType, self.FREQUENCY, self.subscriptions)

    def tick(self):
        """
        Called every tick.
        """
        pass

    def msg_received(self, msg, msg_type):
        """
        This method is called whenever a message is received from the server.
        """
        if msg_type == MsgType.FULL_STATE:
            msg_serialized = msg.SerializeToString()
            if len(self.states) == 0 or msg_serialized != self.states[-1]:
                self.states.append(msg_serialized)
                self.save()

    def save(self):
        """
        Saves the recorded states to a json file.
        """
        with open(self.SAVE_FILE, 'wb') as f:
            for state in self.states:
                f.write(state)
                f.write(b'\n\n\n')


class AutoRoboPlayback(rm.ProtoModule):
    """
    This class provides functionality to record games
    """

    ADDRESS = 'localhost'
    PORT = 11297

    # times per second that tick() and custom_tick() are called
    FREQUENCY = 24
    BACKWARDS = False

    PAUSED = False

    states: list[MsgType.FULL_STATE] = []
    SAVE_FILE = None
    frame = 0

    def __init__(self, addr, port, save_file):
        """
        Builds a new AutoRoboRecorder object.
        @param addr: The address of the server
        @param port: The port of the server
        """
        self.ADDRESS = addr
        self.PORT = port
        self.SAVE_FILE = save_file

        print('Playback game from ' + self.SAVE_FILE)

        self.load()

        self.subscriptions = []
        super().__init__(addr, port, message_buffers, MsgType, self.FREQUENCY, self.subscriptions)
        self.loop.add_reader(sys.stdin, self.keypress)

    def tick(self):
        """
        Called every tick.
        """
        print('Tick = ' + str(self.frame))
        self.write(self.states[self.frame], MsgType.FULL_STATE)
        if self.BACKWARDS:
            self.frame -= 1
        else:
            self.frame += 1
        if self.frame >= len(self.states):
            self.frame = 0

    def msg_received(self, msg, msg_type):
        """
        This method is called whenever a message is received from the server.
        """
        pass

    def load(self):
        """
        Saves the recorded states to a json file.
        """
        with open(self.SAVE_FILE, 'rb') as file:
            content = file.read()
            self.states = content.split(b'\n\n\n')[:-1]

    def keypress(self):
        char = sys.stdin.read(1)
        # For some reason I couldn't quite get this to do what I wanted
        # Still it's a bit cleaner than otherwise
        # sys.stdout.write("\033[F")
        # sys.stdout.write("\033[K")
        # sys.stdout.flush()
        match char:
            case 'p':
                self.FREQUENCY = 0
                self.set_frequency(self.FREQUENCY)
            case 'r':
                self.frame = 0
                self.write(self.states[self.frame], MsgType.FULL_STATE)
            case ',':
                self.frame -= 1
                self.write(self.states[self.frame], MsgType.FULL_STATE)
            case '.':
                self.frame += 1
                self.write(self.states[self.frame], MsgType.FULL_STATE)
            case '<':
                if self.FREQUENCY == 0:
                    self.FREQUENCY = 6
                    self.BACKWARDS = True
                elif self.BACKWARDS:
                    self.FREQUENCY += 6
                else:
                    self.FREQUENCY -= 6
                self.set_frequency(self.FREQUENCY)
            case '>':
                if self.FREQUENCY == 0:
                    self.FREQUENCY = 6
                    self.BACKWARDS = False
                elif self.BACKWARDS:
                    self.FREQUENCY -= 6
                else:
                    self.FREQUENCY += 6
                self.set_frequency(self.FREQUENCY)


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

    parser.add_argument('--record', '-r', type=str, default=None, help='If this is set, this process will record the game to the given json file')
    parser.add_argument('--playback', '-b', type=str, default=None, help='If this is set, this process will playback the game from the given json file')

    args = parser.parse_args()

    if args.record is not None:
        # Create the recorder
        recorder = AutoRoboRecorder(args.address, args.port, args.record)
        recorder.run()

    elif args.playback is not None:
        # Create the playback
        playback = AutoRoboPlayback(args.address, args.port, args.playback)
        playback.run()

    else:
        # Create the server
        server = AutoRobo(args.address, args.port, args.game_engine_path, args.logs_path)

        # User menu
        while True:
            print('''
q) Stop Server
1) Start Game Engine
2) Stop Game Engine
3) Start Visualization
4) Stop Visualization
5) Start Keyboard Input
6) Start Recording
7) Stop Recording
8) Start Playback
p) Pause/Unpause Game
r) Restart Game
''')

            choices = input('Enter your choice: ')

            for choice in choices:
                match choice:
                    case 'q':
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
                        server.start_process('keyboardInput')
                    case '6':
                        server.start_process('recorder')
                    case '7':
                        server.stop_process('recorder')
                    case '8':
                        server.start_process('playback')
                        # playback menu
                        last_choice = 'p'
                        while last_choice != 'q':
                            print('''
q) Stop Playback
p) Pause/Unpause Game
r) Restart Game
,) Previous Frame
.) Next Frame
< ) Decrease Playback Speed
> ) Increase Playback Speed
''')
                            playback_choice = input('Enter your choice: ')
                            if playback_choice == '':
                                playback_choice = last_choice
                            else:
                                last_choice = playback_choice
                            server.send_input('playback', playback_choice)
                        server.stop_process('playback')
                    case 'p':
                        server.send_input('gameEngine', 'p')
                    case 'r':
                        server.send_input('gameEngine', 'r')
                    case _:
                        print('Invalid choice')
