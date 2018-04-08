



def makeDecision(leftListNegative, rightListNegative, upListNegative, 
		downListNegative, leftListPositive rightListPositive, 
		upListPositive, downListNegative):
	
	#the polar coordinate to move  
	return path


def calcPacman(stuff):
	if stuff.thing == basecase:
		return [getWeight(stuff.thing)]
	weight = 1
	out = [0]
	for decision in stuff:
		lst = calcPacman(decision)
		val = lst.pop(0)
		if val >= out[0]:
			out = lst
	return [weight] + lst


def getWeight(loc):
	pass

