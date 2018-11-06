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

class HardCodedPacman(rm.ProtoModule):
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

    def _move_if_valid_dir(self, direction, x, y):
        if direction == right and grid[x + 1][y] not in [I, n]:
            self.pacbot_pos[0] += 1
            self.cur_dir = direction
            return True
        elif direction == left and grid[x - 1][y] not in [I, n]:
            self.pacbot_pos[0] -= 1
            self.cur_dir = direction
            return True
        elif direction == up and grid[x][y + 1] not in [I, n]:
            self.pacbot_pos[1] += 1
            self.cur_dir = direction
            return True
        elif direction == down and grid[x][y - 1] not in [I, n]:
            self.pacbot_pos[1] -= 1
            self.cur_dir = direction
            return True
        return False

    
    def slave(self):
        moves = [up, down, left, right]

        if self.state.mode != LightState.PAUSED:
            if not self._move_if_valid_dir(self.next_dir, self.pacbot_pos[0], self.pacbot_pos[1]):
                self._move_if_valid_dir(self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1])
            else: 
                self.next_dir = moves[random.randint(0,3)]
                self._move_if_valid_dir(self.next_dir, self.pacbot_pos[0], self.pacbot_pos[1])
        pos_buf = PacmanState.AgentState()
        pos_buf.x = self.pacbot_pos[0]
        pos_buf.y = self.pacbot_pos[1]
        pos_buf.direction = self.cur_dir
        self.write(pos_buf.SerializeToString(), MsgType.PACMAN_LOCATION)
    
            
      
    def tick(self): 
        #Set directions the pacman takes
        
        self.slave()        


    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module will connect to the local server
        if msg_type == MsgType.LIGHT_STATE:
            self.state = msg
            if self.state.lives != self.lives:
                self.lives = self.state.lives
                self.pacbot_pos = [pacbot_starting_pos[0], pacbot_starting_pos[1]]
        # This gets called whenever any message is received
        # This module only sends data, so we ignore incoming messages
        # if msg_type == MsgType.FULL_STATE:
        #     self.state = msg
        #     if self.state.lives != self.lives:
        #         self.lives = self.state.lives
        #         self.pacbot_pos = [pacbot_starting_pos[0], pacbot_starting_pos[1]]


def main():
    module = HardCodedPacman(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
