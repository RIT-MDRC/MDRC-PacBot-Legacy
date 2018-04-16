"""
PacbotModule.py
holds all functionality relevant to the game rule's
Ethan Yaccarino-Mims
"""



import os
import robomodules
from .messages import *
from grid import *
from variables import *



#from PacbotBFS import *


ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)
ser = serial.Serial("/dev/ttyACM&", 9600) #replace & with num found from ls /dev/tty/ACM*
ser.baudrate = 9600   

def TURNAROUND():
    return 100


def FREQUENCY():
    return 10


def HITDOT():
    return 1


def HITGHOST():
    return 0


def HITFRUIT():
    return 2


def PATHWEIGHT():
    return 0.95


class PacbotModule(robomodules.ProtoModule):



    def __init__(self, addr, port):
        self.subscriptions = [MsgType.PACMAN_COMMAND]
        super().__init__(addr, port, message_buffers, MsgType,
                         FREQUENCY, self.subscriptions)
        self.state = None
        self.previous_loc = None
        self.direction = PacmanCommand.EAST



    def updateGame(self):
        pacmanLocation = (self.state.pacman.x, self.state.pacman.y)
        if self.grid[self.p_loc[0]][self.p_loc[1]] in [o, O]:
            self.grid[self.p_loc[0]][self.p_loc[1]] = e
        self.tempPLoc = self.p_loc
        self.blueLocation = self.ghost.state.blueGhost.loc
        self.redLocation = self.ghost.state.redGhost.loc
        self.orangeLocation = self.ghost.state.orangeGhost.loc
        self.pinkLocation = self.ghost.state.pinkGhost.loc



    def initTemps(self):
        self.tempBlueLoc = self.blueLocation
        self.tempRedLoc = self.redLocation
        self.tempOrangeLoc = self.orangeLocation
        self.tempPinkLoc = self.pinkLocation
        self.tempDir = self.direction



    def makeCommand(self):
        pass


    def ridePath(self, cmdSet):
        pass
        if self.tempDir == PacmanCommand.EAST:
            self.tempPLoc[0] += 1
            if not self.grid[self.tempPLoc[0]][self.tempPLoc[1]]
        elif self.tempDir == PacmanCommand.WEST:
            self.tempPLoc[0] += 1
        elif self.tempDir == PacmanCommand.NORTH:
            self.tempPLoc[1] -= 1
        elif self.tempDir == PacmanCommand.SOUTH:
            self.tempPLoc[1] += 1




    def findCmdSet(self):
        pass


    def pickDirection(self, cmdSet):
        pass





    def sendString(self, cmd):
        for ch in cmd:
            ser.write(bytes(ch.encode("ascii")))


    def getLine(self):
        return ser.readline()



    def sendDirection(self):
        if True:
            pass



    def makeSplit(self, loc, prior):
        pass




    """
    0: till end, 1: first right, -1: first left,..., 
    TURNAROUND(): turn around
    returns list of 4 instructions read left to right 
    """
    def sendInstructionSet(self):





    def tick(self):

        state = self.server_mo
        if self.state.mode == LightState.RUNNING:
            self.updateGame()

            instructionSet = ()







def main():
    module = PacbotModule(ADDRESS, PORT)
    module.run()


if __name__ == "__main__":
    main()


