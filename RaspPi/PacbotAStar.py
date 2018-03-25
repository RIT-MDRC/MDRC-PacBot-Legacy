"""
PacbotAStar.py
A* search algo for finding distance to an object on the field
Ethan Yaccarino-Mims
"""


"""
heuristic distance between two nodes

@param node1 the first node
@param node2 the second node
"""
def heuristic(node1, node2):
    (x1, y1) = node1
    (x2, y2) = node2

    return abs(x2 - x1) + abs(y2 - y1)



def neighbors(graph, location):
	return ((location[0], location[1] + 1), (location[0] + 1, location[1]),
			(location[0], location[1] - 1), (location[0] - 1, location[1]))



def AStar(grid, start, target):
	frontier = PriorityQueue()
	frontier.put(start, 0)
	cameFrom = {}
	costSoFar = {}
	cameFrom[start] = None
	costSoFar[start] = 0

	while not frontier.empty():
		current = frontier.get()

		if current == target:
			break

		
