#!/usr/bin/env python3

import os, sys, curses, random
import robomodules as rm
from messages import *
from variables import *
from grid import *


ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)

SPEED = 1.0
FREQUENCY = SPEED * game_frequency 

class SimpleWeightsAI(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)

        #pacbot input vars
        self.state = LightState()
        self.pacbot_pos = [pacbot_starting_pos[0], pacbot_starting_pos[1]]
        self.cur_dir = right
        self.next_dir = right
        self.state.mode = LightState.PAUSED
        self.lives = starting_lives


    def tick(self):
        pass


    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.LIGHT_STATE:
            self.state = msg
            if self.state.lives != self.lives:
                self.lives = self.state.lives
                self.pacbot_pos = [pacbot_starting_pos[0], pacbot_starting_pos[1]]

def main():
    module = SimpleWeightsAI(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
