#!/usr/bin/env python3

import os, sys, curses, random
import robomodules as rm
from messages import MsgType, message_buffers, LightState, PacmanCommand
from variables import *
from grid import *
import collections


ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)


FREQUENCY = 30
GOAL_POS = (9,4)

class PacGraph: 
    def __init__(self):
        self.edges = {} 

    def neighbors(self, id): 
        return self.edges[id]

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()
    
    def peek(self):
        return self.elements[0]

    def value(self):
        print(self.elements)

class pacGrid: 
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
    
    #Test whether or not the object is inside the confines of the map
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    #Collision detection for the walls 
    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        #gives the results of available neighbors after filtering out the coordinates that are in_bounds and are passable
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

class HardCodedPacman(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)

        #pacbot input vars
        self.state = None
        self.direction = PacmanCommand.EAST
        self.lives = starting_lives
        self.previous_loc = None 


    # def _move_if_valid_dir(self, direction, x, y):
    #     if direction == right and grid[x + 1][y] not in [I, n]:
    #         self.pacbot_pos[0] += 1
    #         self.cur_dir = direction
    #         return True
    #     elif direction == left and grid[x - 1][y] not in [I, n]:
    #         self.pacbot_pos[0] -= 1
    #         self.cur_dir = direction
    #         return True
    #     elif direction == up and grid[x][y + 1] not in [I, n]:
    #         self.pacbot_pos[1] += 1
    #         self.cur_dir = direction
    #         return True
    #     elif direction == down and grid[x][y - 1] not in [I, n]:
    #         self.pacbot_pos[1] -= 1
    #         self.cur_dir = direction
    #         return True
    #     return False

    def get_direction(self, p_loc, next_loc): 
        if p_loc[0] == next_loc[0]:
            if p_loc[1] < next_loc[1]:
                return PacmanCommand.NORTH
            else:
                return PacmanCommand.SOUTH
        else:
            if p_loc[0] < next_loc[0]:
                return PacmanCommand.EAST
            else:
                return PacmanCommand.WEST

    
    def findPath(self, node, previousNodes, displayGrid, path): 
        if previousNodes[node] == None: 
            return 
        else: 
            if node != GOAL_POS:
                path.append(node)
                displayGrid[node[0]][node[1]] = "0"
            self.findPath(previousNodes[node], previousNodes, displayGrid, path)
            
    def breadth_first_search2(self, graph, start, displayGrid, goal):
        path = []
        theQueue = Queue()
        theQueue.put(start)
        visited = {}
        visited[start] = None
        while(not theQueue.empty()):
            current = theQueue.get()

            if current == goal: 
                self.findPath(current, visited, displayGrid, path)
                break

            #Sets the values to determine where their previous value came from
            #editGrid(displayGrid, current, visited[current])
            for i in graph.neighbors(current):
                if i not in visited: 
                    theQueue.put(i) 
                    visited[i] = current
        return path

    def slave(self):
        moves = [up, down, left, right]

        #print("current and next direction (current, next): ({},{})".format(self.cur_dir, self.next_dir))
        #print("slave location (x,y): ({},{})".format(self.pacbot_pos[0], self.pacbot_pos[1]))

        if self.state.mode != LightState.PAUSED:
            if not self._move_if_valid_dir(self.cur_dir, self.pacbot_pos[0], self.pacbot_pos[1]):
                
                self.next_dir = moves[random.randint(0,3)]

                self._move_if_valid_dir(self.next_dir, self.pacbot_pos[0], self.pacbot_pos[1])


        pos_buf = PacmanState.AgentState()
        pos_buf.x = self.pacbot_pos[0]
        pos_buf.y = self.pacbot_pos[1]
        pos_buf.direction = self.cur_dir

        self.write(pos_buf.SerializeToString(), MsgType.PACMAN_LOCATION)

   #def calculateNext(self):

    #Sending new directions
    def send_direction(self, p_loc, target): 
        new_msg = PacmanCommand()
        new_msg.dir = self.get_direction(p_loc, target)
        self.write(new_msg.SerializeToString(), MsgType.PACMAN_COMMAND)
        
    def _send_stop_command(self):
        new_msg = PacmanCommand()
        new_msg.dir = PacmanCommand.STOP
        self.write(new_msg.SerializeToString(), MsgType.PACMAN_COMMAND)


    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.LIGHT_STATE:
            if self.previous_loc != msg.pacman: 
                if self.previous_loc is not None: 
                    self.direction = self.get_direction((self.previous_loc.x, self.previous_loc.y), (msg.pacman.x, msg.pacman.y))
                self.previous_loc = self.state.pacman if self.state else None 
            self.state = msg


          
    def tick(self): 
        #print(PacmanState().grid) MUST RECIEVE THE PACMAN STATE BEFORE PRINTING GRID
        #Set directions the pacman takes
        #print("pacbot's location (x,y): ({},{})".format(self.state.pacman.x, self.state.pacman.y)) 
        if self.state and self.state.mode == LightState.RUNNING: 
            #Update board
            p_loc = (self.state.pacman.x, self.state.pacman.y)
            next_loc = (self.state.pacman.x + 1, self.state.pacman.y)
            if next_loc != p_loc:
                self.send_direction(p_loc, next_loc)
                return
        self._send_stop_command()




def main():
    module = HardCodedPacman(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
