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


class AutoRobo(rm.ProtoModule):
    """
    This class facilitates running and communication with the services provided by the HarvardURC_Pacbot repo.

    It uses robomodules, a custom library for communicating with the Harvard Robotics Club's server.
    """

    ADDRESS = 'localhost'
    PORT = 11297

    do_record = False

    do_playback = False
    playback_frequency = 24
    playback_backwards = False
    playback_frame = 0

    states: list[MsgType.FULL_STATE] = []
    states_file = None

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
            'file': os.path.basename(__file__),
            'running': False,
            'process': None
        },
        'playback': {
            'file': os.path.basename(__file__),
            'running': False,
            'process': None
        }
    }

    def __init__(self, addr, port, game_engine_path=None, logs_path=None, only_record_file=None, only_playback_file=None):
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

        # this class may start another version of itself dedicated to recording or playback
        if only_record_file is not None or only_playback_file is not None:
            self.subscriptions = [MsgType.FULL_STATE] if only_record_file is not None else []
            super().__init__(addr, port, message_buffers, MsgType, self.playback_frequency, self.subscriptions)
            if only_playback_file is not None:
                self.do_playback = True
                with open(only_playback_file, 'rb') as file:
                    content = file.read()
                    self.states = content.split(b'\n\n\n')[:-1]
                self.loop.add_reader(sys.stdin, self.keypress)
            if only_record_file is not None:
                self.do_record = True
                self.states_file = only_record_file
            self.run()
        else:
            self.start_process('server')
            self.input_loop()

    def input_loop(self):
        while 1:
            help_msg = "\n[Q]uit\nPlay[b]ack"

            if self.processes['gameEngine']['running']:
                help_msg += "\n[K]eyboard Input\n[P]lay/pause\n[R]estart"
                help_msg += "\n\n[ On  ] Game [E]ngine"
            else:
                help_msg += "\n\n[ Off ] Game [E]ngine"

            if self.processes['visualize']['running']:
                help_msg += "\n[ On  ] [V]isualization"
            else:
                help_msg += "\n[ Off ] [V]isualization"

            if self.processes['recorder']['running']:
                help_msg += "\n[ On  ] Re[c]order"
            else:
                help_msg += "\n[ Off ] Re[c]order"

            print(help_msg)
            user_choices = input('\n> ').lower()

            for user_choice in user_choices:
                match user_choice:
                    case 'q':
                        self.stop_process('server')
                        break
                    case 'k':
                        self.start_process('keyboardInput')
                    case 'b':
                        self.start_process('playback')
                        # playback menu
                        last_choice = 'p'
                        while 1:
                            print('\n'
                                  'q) Stop Playback\n'
                                  'p) Pause/Unpause Game\n'
                                  'r) Restart Game\n'
                                  ',) Previous Frame\n'
                                  '.) Next Frame\n'
                                  '< ) Decrease Playback Speed\n'
                                  '> ) Increase Playback Speed\n')
                            playback_choice = input('> ')
                            if playback_choice == '':
                                playback_choice = last_choice
                            else:
                                last_choice = playback_choice
                            if playback_choice == 'q':
                                break
                            self.send_input('playback', playback_choice)
                        self.stop_process('playback')
                    case 'p':
                        if self.processes['gameEngine']['running']:
                            self.send_input('gameEngine', 'p')
                    case 'r':
                        if self.processes['gameEngine']['running']:
                            self.send_input('gameEngine', 'r')
                    case 'e':
                        if self.processes['gameEngine']['running']:
                            self.stop_process('gameEngine')
                        else:
                            self.start_process('gameEngine')
                    case 'v':
                        if self.processes['visualize']['running']:
                            self.stop_process('visualize')
                        else:
                            self.start_process('visualize')
                    case 'c':
                        if self.processes['recorder']['running']:
                            self.stop_process('recorder')
                        else:
                            self.start_process('recorder')
                    case _:
                        pass

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

    # playback only
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

    # playback only
    def tick(self):
        """
        Called every tick.
        """
        if self.do_playback:
            self.write(self.states[self.playback_frame], MsgType.FULL_STATE)
            if self.playback_backwards:
                self.playback_frame -= 1
            else:
                self.playback_frame += 1
            if self.playback_frame >= len(self.states):
                self.playback_frame = 0

    # playback only
    def keypress(self):
        char = sys.stdin.read(1)
        match char:
            case 'p':
                self.playback_frequency = 0
                self.set_frequency(self.playback_frequency)
            case 'r':
                self.playback_frame = 0
                self.write(self.states[self.playback_frame], MsgType.FULL_STATE)
            case ',':
                self.playback_frame -= 1
                self.write(self.states[self.playback_frame], MsgType.FULL_STATE)
            case '.':
                self.playback_frame += 1
                self.write(self.states[self.playback_frame], MsgType.FULL_STATE)
            case '<':
                if self.playback_frequency == 0:
                    self.playback_frequency = 6
                    self.playback_backwards = True
                elif self.playback_backwards:
                    self.playback_frequency += 6
                else:
                    self.playback_frequency -= 6
                self.set_frequency(self.playback_frequency)
            case '>':
                if self.playback_frequency == 0:
                    self.playback_frequency = 6
                    self.playback_backwards = False
                elif self.playback_backwards:
                    self.playback_frequency -= 6
                else:
                    self.playback_frequency += 6
                self.set_frequency(self.playback_frequency)

    # recording only
    def msg_received(self, msg, msg_type):
        if self.do_record and msg_type == MsgType.FULL_STATE:
            msg_serialized = msg.SerializeToString()
            if len(self.states) == 0 or msg_serialized != self.states[-1]:
                self.states.append(msg_serialized)
                with open(self.states_file, 'wb') as f:
                    for state in self.states:
                        f.write(state)
                        f.write(b'\n\n\n')


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

    parser.add_argument('--record', '-r', type=str, default=None,
                        help='[internal use only] If this is set, this process will record the game to the given json '
                             'file')
    parser.add_argument('--playback', '-b', type=str, default=None,
                        help='[internal use only] If this is set, this process will playback the game from the given json '
                             'file')

    args = parser.parse_args()

    # Create the server
    server = AutoRobo(args.address,
                      args.port,
                      args.game_engine_path,
                      args.logs_path,
                      only_record_file=args.record,
                      only_playback_file=args.playback)