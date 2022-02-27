import os, sys, curses, random, copy
import time
import robomodules as rm
from messages import *
from .grid import grid
from .pacBFSHelper import *
# import RPi.GPIO as GPIO
import collections

from .preprocessing.optimized_search import get_dist_and_dir

ADDRESS = "localhost"
PORT = os.environ.get("BIND_PORT", 11295)

FREQUENCY = 2
FEAR = 10
PELLET_WEIGHT = 0.65
SUPER_PELLET_WEIGHT = 0.1        #ADDED weight for super pellets
GHOST_WEIGHT = 0.35
FRIGHTENED_GHOST_WEIGHT = 0.3 * GHOST_WEIGHT
PROXIMITY_PELLET_MULTIPLIER = 0.1
ANTI_CORNER_WEIGHT = 0.1

class HighLevelPacman(rm.ProtoModule):
    def __init__(self, addr, port, game=None, returnInfo=False, frequency_multiplier=1,
                 fear=10, pellet_weight=0.65,super_pellet_weight=.1,ghost_weight=.35,frightened_ghost_weight=.105,
                 proximity_pellet_multiplier=0.1, anti_corner_weight=0.1,
                 runOnClock=True):
        global PELLET_WEIGHT, FEAR, FREQUENCY, SUPER_PELLET_WEIGHT, GHOST_WEIGHT, FRIGHTENED_GHOST_WEIGHT, PROXIMITY_PELLET_MULTIPLIER, ANTI_CORNER_WEIGHT
        FREQUENCY *= frequency_multiplier
        self.game = game
        self.returnInfo = returnInfo
        self.subscriptions = [MsgType.LIGHT_STATE]
        FEAR = fear
        PELLET_WEIGHT = pellet_weight
        SUPER_PELLET_WEIGHT = super_pellet_weight
        GHOST_WEIGHT = ghost_weight
        FRIGHTENED_GHOST_WEIGHT = frightened_ghost_weight
        PROXIMITY_PELLET_MULTIPLIER = proximity_pellet_multiplier
        ANTI_CORNER_WEIGHT = anti_corner_weight
        # with open("botCode/weights.txt", "r") as f:
        #     lines = f.readlines()
        #     values = lines[0].split()
        #     FREQUENCY = float(values[0])
        #     FEAR = float(values[1])
        #     PELLET_WEIGHT = float(values[2])
        #     SUPER_PELLET_WEIGHT = float(values[3])
        #     GHOST_WEIGHT = float(values[4])
        #     FRIGHTENED_GHOST_WEIGHT = float(values[5]) * GHOST_WEIGHT


        if runOnClock:
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
        if self.game is not None:
            self.game.msg_received(new_msg, MsgType.PACMAN_LOCATION)
        else:
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
            if not self.returnInfo:
                print("Moving Right")
            # GPIO.output(37, GPIO.LOW)
            # GPIO.output(35, GPIO.HIGH)
            # GPIO.output(33, GPIO.HIGH)
            # GPIO.output(31, GPIO.HIGH)
            # GPIO.output(29, GPIO.HIGH)
        elif(value == 1):
            if not self.returnInfo:
                print("Moving Left")
            # GPIO.output(37, GPIO.HIGH)
            # GPIO.output(35, GPIO.LOW)
            # GPIO.output(33, GPIO.HIGH)
            # GPIO.output(31, GPIO.HIGH)
            # GPIO.output(29, GPIO.HIGH)
        elif(value == 2):
            if not self.returnInfo:
                print("Moving Up")
            # GPIO.output(37, GPIO.HIGH)
            # GPIO.output(35, GPIO.HIGH)
            # GPIO.output(33, GPIO.LOW)
            # GPIO.output(31, GPIO.HIGH)
            # GPIO.output(29, GPIO.HIGH)
        elif(value == 3):
            if not self.returnInfo:
                print("Moving Down")
            # GPIO.output(37, GPIO.HIGH)
            # GPIO.output(35, GPIO.HIGH)
            # GPIO.output(33, GPIO.HIGH)
            # GPIO.output(31, GPIO.LOW)
            # GPIO.output(29, GPIO.HIGH)
        elif(value == 4):
            if not self.returnInfo:
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

    def get_heuristic_value(self, target):
        if(self.grid[target[0]][target[1]] in [I, n]):
            return None
        pellet_dist = self.find_closest_pellets(self.grid, target, o)
        super_pellet_dist = self.find_closest_pellets(self.grid, target, O)
        ghost_dists = self.find_closest_ghosts(self.grid, target)

        ghost_heuristic = 0
        #print("pellet dist: " + str(pellet_dist))
        pellet_heuristic = pellet_dist * PELLET_WEIGHT
        super_pellet_heuristic = super_pellet_dist * SUPER_PELLET_WEIGHT


# self.state.red_ghost.state != LightState.FRIGHTENED or
#                         self.state.pink_ghost.state != LightState.FRIGHTENED or
#                         self.state.blue_ghost.state != LightState.FRIGHTENED or
#                         self.state.orange_ghost.state != LightState.FRIGHTENED)
        the_ghosts = []
        for i in ghost_dists:
            the_ghosts.append(i[0])

        num_ghost_near_me = 0
        num_ghosts_frightened = 0

        for dist, state in ghost_dists:
            if state == LightState.FRIGHTENED:
                num_ghosts_frightened += 1
                if dist < FEAR:
                    num_ghost_near_me += 1
                    ghost_heuristic += (FEAR - dist)**2 * -1 * FRIGHTENED_GHOST_WEIGHT
            else: # not frightened
                if dist < FEAR:
                    num_ghost_near_me += 1
                    ghost_heuristic += (FEAR - dist)**2 * GHOST_WEIGHT

        super_pellet_heuristic += PROXIMITY_PELLET_MULTIPLIER*num_ghost_near_me
        if num_ghosts_frightened > 0:
            super_pellet_heuristic = 600

        # don't go to corners if ghosts are near me
        anti_corner_heuristic = (abs(target[0]) + abs(target[1])) * num_ghost_near_me * ANTI_CORNER_WEIGHT

        #print("ghost heuristic: " + str(ghost_heuristic))
        #print("pellet heuristic: " + str(pellet_heuristic))
        # print("super pellet heuristic: " + str(super_pellet_heuristic))
        return ghost_heuristic + pellet_heuristic + super_pellet_heuristic + anti_corner_heuristic

    def find_best_location(self, p_loc):
        #self, left, right, down, up
        targets = [p_loc, (p_loc[0] - 1, p_loc[1]), (p_loc[0] + 1, p_loc[1]), (p_loc[0], p_loc[1] - 1), (p_loc[0], p_loc[1] + 1)]
        heuristics = []
        for target in targets:
            heuristics.append(self.get_heuristic_value(target))


        min_heuristic = 99999
        min_target = (0,0)
        for i in range(len(heuristics)):
            if(heuristics[i] != None and (heuristics[i] <= min_heuristic)):
                min_heuristic = heuristics[i]
                min_target = targets[i]

        return min_target

    #Main FUNCTIONALITY
    def tick(self):
        returnInfo = self.returnInfo
        # self.loop.call_later(1.0 / FREQUENCY, self.tick)
        if self.state and self.state.mode == LightState.RUNNING:
            returnState = {}
            if not returnInfo:
                print("\nbegin tick")
            start_time = time.perf_counter()


            # actual code
            self.update_game_state()

            if not returnInfo:
                print(f"time after update game state: {(time.perf_counter() - start_time)*1000:.2f}", )
            else:
                returnState['t1'] = (time.perf_counter() - start_time)*1000
            bestPath = self.find_best_location(self.previousLocation)
            path = breadth_first_search(self.initializedGrid, self.previousLocation, bestPath) #Found by running an algorithm based on previous location
            if not returnInfo:
                print(f"time after bestPath and BFS: {(time.perf_counter() - start_time)*1000:.2f}", )
            else:
                returnState['t2'] = (time.perf_counter() - start_time)*1000
            if path is not None:
                next_location = path[-1]
                if(next_location != self.previousLocation):
                    if(next_location == None):
                        return
                    else:
                        #GET DIRECTION
                        self.print_direction(self.get_direction(next_location, self.previousLocation))
                        returnState['direction'] = self.get_direction(next_location, self.previousLocation)
                        self.send_data(next_location)
            elif(bestPath == self.previousLocation):
                self.print_direction(self.get_direction(bestPath, self.previousLocation))
            if not returnInfo:
                print(f"time after if stack: {(time.perf_counter() - start_time) * 1000:.2f}", )
            else:
                returnState['t3'] = (time.perf_counter() - start_time) * 1000

            # performance tracking
            elapsed_time = time.perf_counter() - start_time
            if not hasattr(self, 'perf_record'):
                self.perf_record = []
            self.perf_record.append(elapsed_time)

            returnState['score'] = self.state.score
            returnState['bfs_cache_info'] = breadth_first_search.cache_info()
            returnState['tf'] = elapsed_time*1000
            returnState['ta'] = sum(self.perf_record)/len(self.perf_record)*1000
            if not returnInfo:
                print("score:", self.state.score)
                print("bfs cache_info:", breadth_first_search.cache_info())
                print(f"tick took {elapsed_time*1000:.2f} ms")
                print(f"average: {sum(self.perf_record)/len(self.perf_record)*1000:.2f} ms")
            else:
                if self.game is not None:
                    self.game.receivePacbotInfo(returnState)
                return returnState
        else:
            self.print_direction(4)
            self.game.receivePacbotInfo({'direction': 4})
            return {'direction': 4}

    #Required to update the GRID, to make sure not to go over the same location
    def update_game_state(self):
        pacLocation = (self.state.pacman.x, self.state.pacman.y)
        if(self.grid[pacLocation[0]][pacLocation[1]] in [o,O]):
            self.grid[pacLocation[0]][pacLocation[1]] = e


    #Gets LIGHT_STATE from local server(Local Server is updated from game Engine)
    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.LIGHT_STATE:
            # if self.game is not None:
            #     pass
            # else:
            self.state = msg
            #Get data from lightstate
            self.previousLocation = (self.state.pacman.x, self.state.pacman.y)



def main():
    try:
        module = HighLevelPacman(ADDRESS, PORT)
        module.run()
    finally:
        # GPIO.cleanup()
        pass

if __name__ == "__main__":
    main()