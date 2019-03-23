import os, sys, curses, random, copy
import robomodules as rm
from messages import *
from variables import *
from grid import grid
from pacBFSHelper import *
import RPi.GPIO as GPIO
import collections

ADDRESS = "129.21.63.16"
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = 10

class highLevelPacman(rm.ProtoModule): 
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.state = None
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(37, GPIO.OUT)
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
    
    def get_direction(self, newLocation, previousLocation): 
        if(newLocation[0] > previousLocation[0]): 
            return right
        elif(newLocation[0] < previousLocation[0]): 
            return left
        elif(newLocation[1] > previousLocation[1]): 
            return up
        elif(newLocation[1] < previousLocation[1]): 
            return down
    
    def print_direction(self, value): 
        if(value == 0): 
            print("Moving Right")
            GPIO.output(37, GPIO.HIGH)
        elif(value == 1): 
            print("Moving Left")
        elif(value == 2): 
            print("Moving Up")
        elif(value == 3): 
            print("Moving Down")
    
    #Main FUNCTIONALITY
    def tick(self):
        if self.state and self.state.mode == LightState.RUNNING:
            next_location = breadth_first_search(initialize_grid(self.grid), self.previousLocation, (15,26)) #Found by running an algorithm based on previous location
            if(next_location != self.previousLocation):
                if(next_location == None):
                    return
                else:
                    #GET DIRECTION
                    self.print_direction(self.get_direction(next_location, self.previousLocation))
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