import threading, asyncio

import robomodules as rm
from messages import MsgType, PacmanState, message_buffers
from sim_canvas import SimCanvas

from typing import Callable

import pacbot_rs


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

    game_state: pacbot_rs.GameState = pacbot_rs.GameState()
    particle_filter: pacbot_rs.ParticleFilter = None
    sim_canvas: SimCanvas = None
    sim_thread: threading.Thread = None

    # The location of the pacman in the maze, as given by the bot code when in simulation
    pacman_fake_location: tuple[int, int] = (1, 1)

    def __init__(self, addr, port, pf: pacbot_rs.ParticleFilter, freq=10,
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
        self.particle_filter = pf
        self.FREQUENCY = freq
        self.custom_tick_light = tick_light
        self.custom_tick_full = tick_full

        # self.start_sim_thread()

        self.subscriptions = [MsgType.LIGHT_STATE, MsgType.FULL_STATE]
        super().__init__(addr, port, message_buffers, MsgType, self.FREQUENCY, self.subscriptions)
        self.state = None

    def start_sim_thread(self):

        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()

        # Set the new event loop as the default for this thread
        asyncio.set_event_loop(loop)

        self.sim_canvas = SimCanvas(self.game_state, self.particle_filter)

    def update_particle_filter(self, particle_filter: pacbot_rs.ParticleFilter):
        if self.sim_canvas is not None:
            self.sim_canvas.update(self.game_state, particle_filter)

    def update_game_state(self):
        """
        Updates the game state with the latest information from the server
        """
        self.game_state.red.pos["current"] = (self.full_state.red_ghost.x, self.full_state.red_ghost.y)
        self.game_state.red.pos["next"] = (self.full_state.red_ghost.x, self.full_state.red_ghost.y)
        # self.game_state.red.frightened_counter = self.full_state.red_ghost.frightened_timer

        self.game_state.pink.pos["current"] = (self.full_state.pink_ghost.x, self.full_state.pink_ghost.y)
        self.game_state.pink.pos["next"] = (self.full_state.pink_ghost.x, self.full_state.pink_ghost.y)
        # self.game_state.pink.frightened_counter = self.full_state.pink_ghost.frightened_timer

        self.game_state.blue.pos["current"] = (self.full_state.blue_ghost.x, self.full_state.blue_ghost.y)
        self.game_state.blue.pos["next"] = (self.full_state.blue_ghost.x, self.full_state.blue_ghost.y)
        # self.game_state.blue.frightened_counter = self.full_state.blue_ghost.frightened_timer

        self.game_state.orange.pos["current"] = (self.full_state.orange_ghost.x, self.full_state.orange_ghost.y)
        self.game_state.orange.pos["next"] = (self.full_state.orange_ghost.x, self.full_state.orange_ghost.y)
        # self.game_state.orange.frightened_counter = self.full_state.orange_ghost.frightened_timer


        self.game_state.state = [
            2,  # PacmanState enum 0 [CHASE] translates to GameStateState enum 2
            1,  # PacmanState enum 1 [SCATTER] translates to GameStateState enum 1
            3,  # PacmanState enum 2 [FRIGHTENED] translates to GameStateState enum 3
            2,  # PacmanState enum 3 [PAUSED] translates to default GameStateState enum 2
        ][self.full_state.mode]

        for row in range(28):
            for col in range(31):
                if self.game_state.grid[row][col] == 5:  # don't overwrite ghost spawn locations
                    continue
                self.game_state.grid[row][col] = [
                    1,  # PacmanState enum 0 [WALL] translates to GridValue enum 1
                    2,  # PacmanState enum 1 [PELLET] translates to GridValue enum 2
                    4,  # PacmanState enum 2 [POWER_PELLET] translates to GridValue enum 4
                    3,  # PacmanState enum 3 [EMPTY] translates to GridValue enum 3
                    6,  # PacmanState enum 4 [CHERRY] translates to GridValue enum 6
                ][self.full_state.grid[row * 31 + col]]

        self.game_state.frightened_counter = self.full_state.frightened_timer
        self.game_state.score = self.full_state.score
        self.game_state.play = self.full_state.mode != self.full_state.PAUSED
        self.game_state.update_ticks = self.full_state.update_ticks
        self.game_state.lives = self.full_state.lives
        # self.game_state.ticks_since_spawn = ???

    def msg_received(self, msg, msg_type):
        """
        This method is called whenever a message is received from the server.
        """
        if msg_type == MsgType.LIGHT_STATE:
            self.light_state = msg
        elif msg_type == MsgType.FULL_STATE:
            self.full_state = msg
            self.update_game_state()

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
        self.game_state.pacbot.update((round(location[0]), round(location[1])))

        new_msg = PacmanState.AgentState()
        # Required X and Y location
        new_msg.x = round(self.pacman_fake_location[0])
        new_msg.y = round(self.pacman_fake_location[1])

        self.write(new_msg.SerializeToString(), MsgType.PACMAN_LOCATION)