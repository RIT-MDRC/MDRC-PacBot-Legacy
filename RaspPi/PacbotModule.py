"""
PacbotModule.py
holds all functionality relevant to the game rule's
Ethan Yaccarino-Mims
"""

import os
from .messages import *
from grid import *

#from PacbotBFS import *


ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)
ser = serial.Serial("/dev/ttyACM&", 9600) #replace & with num found from ls /dev/tty/ACM*
ser.baudrate = 9600   

def TURNAROUND():
	return 100


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
        self.comms = 


	def updateGame(self):
		pacmanLocation = (self.state.pacman.x, self.state.pacman.y)
		if self.grid[p_loc[0]][p_loc[1]] in [o, O]:
			self.grid[p_loc[0]][p_loc[1]] = e
		self.blueLocation = ghost.state.blueGhost
		self.redLocation = ghost.state.redGhost
		self.orangeLocation = ghost.state.orangeGhost
		self.pinkLocation = ghost.state.pinkGhost




    def makeCommand():





	def buildGraph(grid):
		for x in range(len(grid)):
			for y in range(len(grid[0])):
				pass




    def sendString(self, cmd):
        for ch in cmd:
            ser.write(bytes(ch.encode("ascii")))


    def getLine(self):
        return ser.readline()



    def sendDirection():
        if()



	def makeSplit(loc, prior):
		pass


        

	"""
	0: till end, 1: first right, -1: first left,..., 
	TURNAROUND(): turn around
	returns list of 4 instructions read left to right 
	"""
	def getInstructionSet():





	def tick(self):

        state = self.server_mo
		if self.state.mode == LightState.RUNNING:
			self.updateGame()

			instructionSet = findBestDirection()







def main():
	module = PacbotModule(ADDRESS, PORT)
	module.run()


if __name == "__main__":
	main()


