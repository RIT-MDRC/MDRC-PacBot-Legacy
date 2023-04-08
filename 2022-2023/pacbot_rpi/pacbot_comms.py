import robomodules as rm
from messages import MsgType, PacmanState, message_buffers

from typing import Callable

class AutoRoboClient(rm.ProtoModule):
    """
    This class acts as a client to the AutoRobo class.
    """

    ADDRESS = 'localhost'
    PORT = 11297

    # times per second that tick() and custom_tick() are called
    FREQUENCY = 10
    custom_tick_light: Callable[[MsgType.LIGHT_STATE], None] = None
    custom_tick_full: Callable[[MsgType.FULL_STATE], None] = None

    light_state: MsgType.LIGHT_STATE = None
    full_state: MsgType.FULL_STATE = None

    # The location of the pacman in the maze, as given by the bot code when in simulation
    pacman_fake_location: tuple[int, int] = (1, 1)

    def __init__(self, addr, port, freq=10,
                 tick_light: Callable[[MsgType.LIGHT_STATE], None] = None,
                 tick_full: Callable[[MsgType.FULL_STATE], None] = None):
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
        self.custom_tick_light = tick_light
        self.custom_tick_full = tick_full

        self.subscriptions = [MsgType.LIGHT_STATE, MsgType.FULL_STATE]
        super().__init__(addr, port, message_buffers, MsgType, self.FREQUENCY, self.subscriptions)
        self.state = None

    def msg_received(self, msg, msg_type):
        """
        This method is called whenever a message is received from the server.
        """
        if msg_type == MsgType.LIGHT_STATE:
            self.light_state = msg
        elif msg_type == MsgType.FULL_STATE:
            self.full_state = msg

    def tick(self):
        """
        This method is called every tick.
        """
        if self.custom_tick_light is not None and self.light_state is not None:
            self.custom_tick_light(self.light_state)
        if self.custom_tick_full is not None and self.full_state is not None:
            self.custom_tick_full(self.full_state)

    def update_fake_location(self, location: tuple[int, int]):
        """
        This method can be called by the bot code to update Pacbot's location
        """
        self.pacman_fake_location = location

        new_msg = PacmanState.AgentState()
        # Required X and Y location
        new_msg.x = self.pacman_fake_location[0]
        new_msg.y = self.pacman_fake_location[1]

        self.write(new_msg.SerializeToString(), MsgType.PACMAN_LOCATION)