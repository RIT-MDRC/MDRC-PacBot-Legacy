import os, sys, curses, random, copy
import time
import robomodules as rm
from messages import *
from variables import *
from grid import grid
from pacBFSHelper import *
# import RPi.GPIO as GPIO
import collections

from preprocessing.optimized_search import get_dist_and_dir

ADDRESS = "localhost"
if len(sys.argv) == 1:
    PORT = os.environ.get("BIND_PORT", 11295)
else:
    PORT = os.environ.get("BIND_PORT", int(sys.argv[1]))
 
FREQUENCY = 8
FEAR = 10
PELLET_WEIGHT = 0.65
SUPER_PELLET_WEIGHT = 0.1        #ADDED weight for super pellets
GHOST_WEIGHT = 0.35
FRIGHTENED_GHOST_WEIGHT = 0.3 * GHOST_WEIGHT

class highLevelPacman(rm.ProtoModule): 
    def __init__(self, addr, port):
        global PELLET_WEIGHT, FEAR, FREQUENCY, SUPER_PELLET_WEIGHT, GHOST_WEIGHT, FRIGHTENED_GHOST_WEIGHT
        self.subscriptions = [MsgType.LIGHT_STATE]
        with open("botCode/weights.txt", "r") as f:
            lines = f.readlines()
            values = lines[0].split()
            FREQUENCY = float(values[0])
            FEAR = float(values[1])
            PELLET_WEIGHT = float(values[2])
            SUPER_PELLET_WEIGHT = float(values[3])
            GHOST_WEIGHT = float(values[4])
            FRIGHTENED_GHOST_WEIGHT = float(values[5]) * GHOST_WEIGHT


        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.state = None
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(37, GPIO.OUT, initial=GPIO.HIGH)
        # GPIO.setup(35, GPIO.OUT, initial=GPIO.HIGH)
        # GPIO.setup(33, GPIO.OUT, initial=GPIO.HIGH)
        # GPIO.setup(31, GPIO.OUT, initial=GPIO.HIGH)
        # GPIO.setup(29, GPIO.OUT, initial=GPIO.HIGH)
        #self declared variables
        self.previousLocation = None  
        self.grid = copy.deepcopy(grid)
        self.initializedGrid = initialize_grid(self.grid)

    #Sends pacman data to local server which then communicates with game engine
    def send_data(self, pacmanLocation):
        new_msg = PacmanState.AgentState()
        #Required X and Y location 
        new_msg.x = pacmanLocation[0]
        new_msg.y = pacmanLocation[1]
        self.write(new_msg.SerializeToString(), MsgType.PACMAN_LOCATION)
    
    def get_direction(self, newLocation, previousLocation): 
        if(newLocation[0] == previousLocation[0] and 
            newLocation[1] == previousLocation[1]): 
            return stop
        elif(newLocation[1] == previousLocation[1]):
            if(newLocation[0] > previousLocation[0]): 
                return right
            elif(newLocation[0] < previousLocation[0]): 
                return left
        elif(newLocation[0] == previousLocation[0]): 
            if(newLocation[1] > previousLocation[1]): 
                return up
            elif(newLocation[1] < previousLocation[1]): 
                return down 
    
    def print_direction(self, value):
        if(value == 0): 
            print("Moving Right")
            # GPIO.output(37, GPIO.LOW)
            # GPIO.output(35, GPIO.HIGH)
            # GPIO.output(33, GPIO.HIGH)
            # GPIO.output(31, GPIO.HIGH)
            # GPIO.output(29, GPIO.HIGH)
        elif(value == 1): 
            print("Moving Left")
            # GPIO.output(37, GPIO.HIGH)
            # GPIO.output(35, GPIO.LOW)
            # GPIO.output(33, GPIO.HIGH)
            # GPIO.output(31, GPIO.HIGH)
            # GPIO.output(29, GPIO.HIGH)
        elif(value == 2): 
            print("Moving Up")
            # GPIO.output(37, GPIO.HIGH)
            # GPIO.output(35, GPIO.HIGH)
            # GPIO.output(33, GPIO.LOW)
            # GPIO.output(31, GPIO.HIGH)
            # GPIO.output(29, GPIO.HIGH)
        elif(value == 3): 
            print("Moving Down")
            # GPIO.output(37, GPIO.HIGH)
            # GPIO.output(35, GPIO.HIGH)
            # GPIO.output(33, GPIO.HIGH)
            # GPIO.output(31, GPIO.LOW)
            # GPIO.output(29, GPIO.HIGH)
        elif(value == 4): 
            print("Stop")
            # GPIO.output(37, GPIO.HIGH)
            # GPIO.output(35, GPIO.HIGH)
            # GPIO.output(33, GPIO.HIGH)
            # GPIO.output(31, GPIO.HIGH)
            # GPIO.output(29, GPIO.LOW)
    
    def print_grid_enum(self, value): 
        if(value == 1):
            print("I")
        elif(value == 2):
            print("o")
        elif(value == 3): 
            print("e")
        elif(value == 4):
            print("0")
        elif(value == 5): 
            print("n")
    
    def find_closest_ghosts(self, grid, pacmanLocation): 
        results = []
        for ghost in [self.state.red_ghost, self.state.pink_ghost, self.state.orange_ghost, self.state.blue_ghost]:
            res = get_dist_and_dir(pacmanLocation, (ghost.x, ghost.y))
            if res is not None:
                results.append((res[0], ghost.state))
        return results

    #can change into BFS
    def find_closest_pellets(self, grid, loc, n):
        paths = bfs_find_pellet(self.initializedGrid, grid, loc, n)
        if(paths != None):
            return len(paths)
        else: 
            return 0

    def find_best_location(self, p_loc):
        #self, left, right, down, up
        targets = [p_loc, (p_loc[0] - 1, p_loc[1]), (p_loc[0] + 1, p_loc[1]), (p_loc[0], p_loc[1] - 1), (p_loc[0], p_loc[1] + 1)]
        heuristics = []
        for target in targets: 
            if(self.grid[target[0]][target[1]] in [I, n]):
                heuristics.append(None)
                continue
            pellet_dist = self.find_closest_pellets(self.grid, target, o)
            super_pellet_dist = self.find_closest_pellets(self.grid, target, O)
            ghost_dists = self.find_closest_ghosts(self.grid, target)

            ghost_heuristic = 0 
            #print("pellet dist: " + str(pellet_dist))
            pellet_heuristic = pellet_dist * PELLET_WEIGHT
            #super_pellet_heuristic = super_pellet_dist * SUPER_PELLET_WEIGHT //commented out to allow super-pellet weight to calculate based on ghosts


# self.state.red_ghost.state != LightState.FRIGHTENED or
#                         self.state.pink_ghost.state != LightState.FRIGHTENED or
#                         self.state.blue_ghost.state != LightState.FRIGHTENED or 
#                         self.state.orange_ghost.state != LightState.FRIGHTENED)
            the_ghosts = []
            for i in ghost_dists: 
                the_ghosts.append(i[0])

            super_pellet_heuristic = super_pellet_dist //* .1
            for value in ghost_dists: 
                if value[0] < FEAR: 
                    if(value[1] != LightState.FRIGHTENED):
                        ghost_heuristic += pow(FEAR - min(the_ghosts), 2) * GHOST_WEIGHT
                        if(super_pellet_dist < FEAR):
                            super_pellet_heuristic = super_pellet_dist * SUPER_PELLET_WEIGHT
                    else: 
                        ghost_heuristic += pow(FEAR - min(the_ghosts), 2) * -1 * FRIGHTENED_GHOST_WEIGHT

            #print("ghost heuristic: " + str(ghost_heuristic))
            #print("pellet heuristic: " + str(pellet_heuristic))
            heuristics.append(ghost_heuristic + pellet_heuristic + super_pellet_heuristic)

        min_heuristic = 99999
        min_target = (0,0)
        for i in range(len(heuristics)):
            if(heuristics[i] != None and (heuristics[i] <= min_heuristic)): 
                min_heuristic = heuristics[i]
                min_target = targets[i]

        return min_target

    #Main FUNCTIONALITY
    def tick(self):
        if self.state and self.state.mode == LightState.RUNNING:
            print("\nbegin tick")
            start_time = time.perf_counter()
            
            # actual code
            self.update_game_state()
            print(f"time after update game state: {(time.perf_counter() - start_time)*1000:.2f}", )
            bestPath = self.find_best_location(self.previousLocation)
            path = breadth_first_search(self.initializedGrid, self.previousLocation, bestPath) #Found by running an algorithm based on previous location
            print(f"time after bestPath and BFS: {(time.perf_counter() - start_time)*1000:.2f}", )
            if path is not None:
                next_location = path[-1]
                if(next_location != self.previousLocation):
                    if(next_location == None):
                        return
                    else:
                        #GET DIRECTION
                        self.print_direction(self.get_direction(next_location, self.previousLocation))
                        self.send_data(next_location)
            elif(bestPath == self.previousLocation): 
                self.print_direction(self.get_direction(bestPath, self.previousLocation))
            print(f"time after if stack: {(time.perf_counter() - start_time) * 1000:.2f}", )
            
            # performance tracking
            elapsed_time = time.perf_counter() - start_time
            if not hasattr(self, 'perf_record'):
                self.perf_record = []
            self.perf_record.append(elapsed_time)
            print("score:", self.state.score)
            print("bfs cache_info:", breadth_first_search.cache_info())
            print(f"tick took {elapsed_time*1000:.2f} ms")
            print(f"average: {sum(self.perf_record)/len(self.perf_record)*1000:.2f} ms")
        else:
            self.print_direction(4)

    #Required to update the GRID, to make sure not to go over the same location
    def update_game_state(self):
        pacLocation = (self.state.pacman.x, self.state.pacman.y)
        if(self.grid[pacLocation[0]][pacLocation[1]] in [o,O]):
            self.grid[pacLocation[0]][pacLocation[1]] = e
        
    
    #Gets LIGHT_STATE from local server(Local Server is updated from game Engine)
    def msg_received(self, msg, msg_type): 
        if msg_type == MsgType.LIGHT_STATE:
            self.state = msg
            #Get data from lightstate 
            self.previousLocation = (self.state.pacman.x, self.state.pacman.y)



def main():
    try:
        module = highLevelPacman(ADDRESS, PORT)
        module.run()
    finally:
        # GPIO.cleanup()
        pass

if __name__ == "__main__":
    main()
