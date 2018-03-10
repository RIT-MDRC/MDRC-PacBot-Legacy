"""
MDRC Pacbot AI 
uses Neural Evalution through Augmenting Topolodgies
Credit goes to Sethblings MarI/O for much of the design elements 
Ethan Yaccarino-Mims
"""
import pacman
import 


moves = ["Up", "Down", "Left", "Right"]
moveDirections = {"Up": 90, "Down": 270, "Left": 180, "Right": 0}

Inputs = 32*28 + 1 #size of field
Outputs = len(moves)


Population = 100
DeltaDisjoint = 2.0
DeltaWeights = 0.4
DeltaThreshold = 1.0
StaleSpecies = 10
MutateConnectionsChance = 0.25
PerturbChance = 0.90
CrossoverChance = 0.75
LinkMutationChance = 2.0
NodeMutationChance = 0.50
BiasMutationChance = 0.40
StepSize = 0.1
DisableMutationChance = 0.4
EnableMutationChance = 0.2
TimeoutConstant = 20
MaxNodes = 1000000

"""
gets the positions of all needed sprites

@return the positions of the sprites as a dictionary
"""
def getPositions():
	pacmanPos = (pacman.getX(), pacman.getY())
	redPos = (ghosts.getRedX(), ghosts.getRedY())
	orangePos = (ghosts.getOrangeX(), ghosts.getOrangeY())
	bluePos = (ghosts.getBlueX(), ghosts.getBlueY())
	pinkPos = (ghosts.getPinkX(), ghosts.getPinkY())
	positions = {"Pacman": pacmanPos, "Red": redPos, "Blue": bluePos,
				"Orange": orangePos, "Pink": pinkPos}
	return positions
	

"""
@return the tile at (x,y)
"""
def getTile(x, y):
	return grid[x][y]



def getInputs():
	positions = getPositions()
	inputs = list()

	for x in range(32):
		for y in range(28):
			inputs[len(inputs) + 1] = 0

			tile = getTile(x, y)
			if tile == 1 and positions["Mario"][0] 



























	