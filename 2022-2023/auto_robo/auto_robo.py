# @author Michael Elia
# @date 2023-04-06

import os
import robomodules as rm
import argparse as ap

from Pacbot.src.gameEngine.messages import *

from typing import Callable


class AutoRobo:
    """
    This class facilitates running and communication with the services provided by the HarvardURC_Pacbot repo.

    It uses robomodules, a custom library for communicating with the Harvard Robotics Club's server.
    """

    def __init__(self):
        pass


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

    args = parser.parse_args()

    # Create the client
    client = AutoRoboClient(args.address, args.port)
