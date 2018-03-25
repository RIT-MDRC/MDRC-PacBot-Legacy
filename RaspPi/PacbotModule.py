"""
PacbotModule.py
holds all functionality relevant to the game rule's
Ethan Yaccarino-Mims
"""

import os
import robomodules
from messages *
from grid import grid


ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)


def FREQUENCY():
    return 10


class PacbotModule(robomodules.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.PACMAN_COMMAND]
        super().__init__(addr, port, message_buffers, MsgType, 
        				 FREQUENCY, self.subscriptions)
        self.state = None
        self.previous_loc = None
        self.direction = PacmanCommand.EAST
        self.grid = copy.deepcopy(grid)


    def updateGame(self):
    	pacmanLocation = (self.state.pacman.x, self.state.pacman.y)
    	if self.grid[p_loc[0]][p_loc[1]] in [o, O]:
            self.grid[p_loc[0]][p_loc[1]] = e
        blueLocation = ()





    def tick(self):
    	if self.state.mode == LightState.RUNNING:
    		self.updateGame()







def main():
	module = PacbotModule(ADDRESS, PORT)
	module.run()


if __name == "__main__":
	main()


