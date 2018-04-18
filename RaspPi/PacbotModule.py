#!/usr/bin/env python3

"""
PacbotModule.py
holds all functionality relevant to the game rule's
Ethan Yaccarino-Mims
"""

import os
import serial
import RPi.GPIO as GPIO
import robomodules
from .messages import *
from grid import *
from variables import *


ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)
ser = serial.Serial("/dev/ttyACM&", 9600) #replace & with num found from ls /dev/tty/ACM*
ser.baudrate = 9600   

def TURNAROUND():
    return 100


def FREQUENCY():
    return 10


def HITDOT():
    return 1.5


def HITGHOST():
    return 0


def HITFRUIT():
    return 2


def PATHWEIGHT():
    return 0.98


def HITLIGHT():
    return 3


def MINWEIGHT():
    return 0.5


class PacbotModule(robomodules.ProtoModule):



    def __init__(self, addr, port):
        self.subscriptions = [MsgType.PACMAN_COMMAND]
        super().__init__(addr, port, message_buffers, MsgType,
                         FREQUENCY, self.subscriptions)
        self.state = None
        self.last_p_loc = None
        self.direction = PacmanCommand.EAST



    def updateGame(self):
        self.pacmanLocation = (self.state.pacman.x, self.state.pacman.y)
        if self.grid[self.p_loc[0]][self.p_loc[1]] in [2, 4]:
            self.grid[self.p_loc[0]][self.p_loc[1]] = 3
        self.blueLocation = self.ghost.state.blueGhost.loc
        self.redLocation = self.ghost.state.redGhost.loc
        self.orangeLocation = self.ghost.state.orangeGhost.loc
        self.pinkLocation = self.ghost.state.pinkGhost.loc


    def makeCommand(self):
        ghostLocs = [self.pinkLocation[:][:], self.orangeLocation[:][:],
                     self.redLocation[:][:], self.blueLocation[:][:]]
        loc = self.p_loc[:][:]
        cmdSet = [1]
        path = self.pickDirection(cmdSet, loc, self.direction, ghostLocs)

        return path


    def ridePath(self, cmdSet, location, direction, ghostLocs):

        for ghostLoc in ghostLocs:
            ghostLoc = self.calcGhostMoves(ghostLoc, location)

        if(cmdSet[0] < MINWEIGHT()):
            return [0].extend(cmdSet[1:])

        if direction == PacmanCommand.EAST:
            dir = 1
            axis = 0
        elif direction == PacmanCommand.WEST:
            dir = -1
            axis = 0
        elif direction == PacmanCommand.NORTH:
            dir = -1
            axis = 1
        else:
            dir = 1
            axis = 1

        if axis == 0:
            lr = 0
            ud = 1
        else:
            lr = 1
            ud = 0

        totalWeight = cmdSet[0]

        location[axis] += dir
        while not self.grid[location[0] + ud][location[1] + lr] in [2, 3, 4] and \
                not self.grid[location[0] - ud][location[1] - lr] in [2, 3, 4]:
            if location in ghostLocs:
                return [HITGHOST()].extend(cmdSet[1:])
            elif self.grid[location[0]][location[1]] == 2:
                return [HITDOT()].extend(cmdSet[1:])
            elif self.grid[location[0]][location[1]] == 4:
                return [HITLIGHT()].extend(cmdSet[1:])
            elif self.grid[location[0]][location[1]] == 3:
                totalWeight *= PATHWEIGHT()

            location[axis] += dir

        return self.pickDirection([totalWeight].extend(cmdSet[1:]), location[:][:],
                                  direction, ghostLocs[:][:][:])


    def pickDirection(self, cmdSet, loc, dir, ghostLocs):
        cmds = list()

        #most disgusting code that I have ever wrote
        if dir == PacmanCommand.EAST:
            if self.grid[loc[0] + 1][loc[1]] in [2, 3, 4]:
                cmds.append(self.ridePath(cmdSet.append(1), loc, PacmanCommand.SOUTH, ghostLocs))
            if self.grid[loc[0] - 1][loc[1]] in [2, 3, 4]:
                cmds.append(self.ridePath(cmdSet.append(-1), loc, PacmanCommand.NORTH, ghostLocs))
            if self.grid[loc[0]][loc[1] + 1] in [2, 3, 4]:
                cmds.append(self.ridePath(cmdSet.append(0), loc, PacmanCommand.EAST, ghostLocs))
            if len(cmds) == 0:
                cmds.append(self.ridePath(cmdSet.append(180), loc, PacmanCommand.WEST, ghostLocs))
        elif dir == PacmanCommand.WEST:
            if self.grid[loc[0] - 1][loc[1]] in [2, 3, 4]:
                cmds.append(self.ridePath(cmdSet.append(1), loc, PacmanCommand.NORTH, ghostLocs))
            if self.grid[loc[0] + 1][loc[1]] in [2, 3, 4]:
                cmds.append(self.ridePath(cmdSet.append(-1), loc, PacmanCommand.SOUTH, ghostLocs))
            if self.grid[loc[0]][loc[1] - 1] in [2, 3, 4]:
                cmds.append(self.ridePath(cmdSet.append(0), loc, PacmanCommand.WEST, ghostLocs))
            if len(cmds) == 0:
                cmds.append(self.ridePath(cmdSet.append(180), loc, PacmanCommand.EAST, ghostLocs))
        elif dir == PacmanCommand.NORTH:
            if self.grid[loc[0]][loc[1] + 1] in [2, 3, 4]:
                cmds.append(self.ridePath(cmdSet.append(1), loc, PacmanCommand.EAST, ghostLocs))
            if self.grid[loc[0]][loc[1] - 1] in [2, 3, 4]:
                cmds.append(self.ridePath(cmdSet.append(-1), loc, PacmanCommand.WEST, ghostLocs))
            if self.grid[loc[0] - 1][loc[1]] in [2, 3, 4]:
                cmds.append(self.ridePath(cmdSet.append(0), loc, PacmanCommand.NORTH, ghostLocs))
            if len(cmds) == 0:
                cmds.append(self.ridePath(cmdSet.append(180), loc, PacmanCommand.SOUTH, ghostLocs))
        else:
            if self.grid[loc[0]][loc[1] - 1] in [2, 3, 4]:
                cmds.append(self.ridePath(cmdSet.append(1), loc, PacmanCommand.WEST, ghostLocs))
            if self.grid[loc[0]][loc[1] + 1] in [2, 3, 4]:
                cmds.append(self.ridePath(cmdSet.append(-1), loc, PacmanCommand.EAST, ghostLocs))
            if self.grid[loc[0] + 1][loc[1]] in [2, 3, 4]:
                cmds.append(self.ridePath(cmdSet.append(0), loc, PacmanCommand.SOUTH, ghostLocs))
            if len(cmds) == 0:
                cmds.append(self.ridePath(cmdSet.append(180), loc, PacmanCommand.NORTH, ghostLocs))

        bestPath = cmds[0]

        for path in cmds:
            if path[0] > bestPath[0]:
                bestPath = path


        return bestPath


    def calcGhostMoves(self, tempGhostLoc, tempPacLoc):
        verticalDistance = tempGhostLoc[0] - tempPacLoc[0]
        horizontalDistance = tempGhostLoc[1] - tempPacLoc[1]
        if horizontalDistance > 0 and verticalDistance > 0:
            up = abs(verticalDistance)
            left = abs(horizontalDistance)
            down = 100
            right = 100
        elif horizontalDistance > 0:
            down = abs(verticalDistance)
            left = abs(horizontalDistance)
            up = 100
            right = 100
        elif verticalDistance > 0:
            up = abs(verticalDistance)
            right = abs(horizontalDistance)
            down = 100
            left = 100
        else:
            down = abs(verticalDistance)
            right = abs(horizontalDistance)
            up = 100
            left = 100

        dirs = [right, left, up, down]
        dirs.sort()

        if dirs[0] == down:
            if self.grid[tempGhostLoc[0] + 1][tempGhostLoc[1]] in [2, 3, 4]:
                tempGhostLoc[0] += 1
            elif dirs[1] == left:
                if self.grid[tempGhostLoc[0]][tempGhostLoc[1] - 1] in [2, 3, 4]:
                    tempGhostLoc[1] -= 1
            elif dirs[1] == right:
                if self.grid[tempGhostLoc[0]][tempGhostLoc[1] + 1] in [2, 3, 4]:
                    tempGhostLoc[1] += 1
        elif dirs[0] == up:
            if self.grid[tempGhostLoc[0] - 1][tempGhostLoc[1]] in [2, 3, 4]:
                tempGhostLoc[0] -= 1
            elif dirs[1] == left:
                if self.grid[tempGhostLoc[0]][tempGhostLoc[1] - 1] in [2, 3, 4]:
                    tempGhostLoc[1] -= 1
            elif dirs[1] == right:
                if self.grid[tempGhostLoc[0]][tempGhostLoc[1] + 1] in [2, 3, 4]:
                    tempGhostLoc[1] += 1
        elif dirs[0] == left:
            if self.grid[tempGhostLoc[0]][tempGhostLoc[1] - 1] in [2, 3, 4]:
                tempGhostLoc[1] -= 1
            elif dirs[1] == up:
                if self.grid[tempGhostLoc[0] - 1][tempGhostLoc[1]] in [2, 3, 4]:
                    tempGhostLoc[0] -= 1
            elif dirs[1] == down:
                if self.grid[tempGhostLoc[0] + 1][tempGhostLoc[1]] in [2, 3, 4]:
                    tempGhostLoc[0] += 1
        elif dirs[0] == right:
            if self.grid[tempGhostLoc[0]][tempGhostLoc[1] + 1] in [2, 3, 4]:
                tempGhostLoc[1] += 1
            elif dirs[1] == up:
                if self.grid[tempGhostLoc[0] - 1][tempGhostLoc[1]] in [2, 3, 4]:
                    tempGhostLoc[0] -= 1
            elif dirs[1] == down:
                if self.grid[tempGhostLoc[0] + 1][tempGhostLoc[1]] in [2, 3, 4]:
                    tempGhostLoc[0] += 1

        return tempGhostLoc



    def sendString(self, cmd):
        for ch in cmd:
            ser.write(bytes(ch.encode("ascii")))


    def getLine(self):
        return ser.readline()


    """
    0: till end, 1: first right, -1: first left,..., 
    TURNAROUND(): turn around
    returns list of 4 instructions read left to right 
    """
    def sendInstructionSet(self, cmdSet):
        for cmd in cmdSet[1:]:
            ser.write(bytes(cmd.encode("ascii")))




    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.LIGHT_STATE:
            if self.last_p_loc != self.p_loc:
                if self.last_p_loc != None:
                    if self.p_loc[0] == self.last_p_loc[0]:
                        if self.p_loc[1] > self.last_p_loc[1]:
                            self.direction = PacmanCommand.EAST
                        else:
                            self.direction = PacmanCommand.WEST
                    else:
                        if self.p_loc[0] > self.last_p_loc[0]:
                            self.direction = PacmanCommand.SOUTH
                        else:
                            self.direction = PacmanCommand.NORTH
                    self.last_p_loc = self.state.pacman
            self.state = msg



    def tick(self):
        if self.state == None:
            pass



        state = self.server_mode
        if self.state.mode == LightState.RUNNING:
            self.updateGame()








def main():
    module = PacbotModule(ADDRESS, PORT)
    module.run()


if __name__ == "__main__":
    main()


