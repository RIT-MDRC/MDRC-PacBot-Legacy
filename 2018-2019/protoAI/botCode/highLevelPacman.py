import os, sys, curses, random, copy
import robomodules as rm
from messages import *
from variables import *
from grid import grid
import collections

ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = 10

class highLevelPacman(rm.ProtoModule): 
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.state = None

        #self declared variables
        self.previousLocation = None  
        self.grid = copy.deepcopy(grid)

    #Sends pacman data to local server which then communicates with game engine
    def send_data(self, pacmanLocation):
        new_msg = PacmanState.AgentState()
        #Required X and Y location 
        new_msg.x = pacmanLocation[0]
        new_msg.y = pacmanLocation[1]
        self.write(new_msg.SerializeToString(), MsgType.PACMAN_LOCATION)

    #Main FUNCTIONALITY
    def tick(self):
        if self.state and self.state.mode == LightState.RUNNING:
            next_location = (15,7) #Found by running an algorithm based on previous location
            self.send_data(next_location)

    #Required to update the GRID, to make sure not to go over the same location
    #def update_game_state(self):
        
    
    #Gets LIGHT_STATE from local server(Local Server is updated from game Engine)
    def msg_received(self, msg, msg_type): 
        if msg_type == MsgType.LIGHT_STATE:
            self.state = msg
            #Get data from lightstate 
            self.previousLocation = (self.state.pacman.x, self.state.pacman.y)



def main():
    module = highLevelPacman(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()