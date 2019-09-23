import collections
from variables import *

#Used for grid Initialization
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

def findPath(node, previousNodes, path):
    if previousNodes[node] == None: 
        return 
    else: 
        path.append(node)
        findPath(previousNodes[node], previousNodes, path)
        
def breadth_first_search(graph, start, goal):
    path = []
    theQueue = collections.deque()
    theQueue.append(start)
    visited = {}
    visited[start] = None
    while theQueue:
        current = theQueue.popleft()
        #Stops and returns the best path
        if current == goal:
            findPath(current, visited, path)
            break
        
        #Looks for paths
        for i in graph.neighbors(current):
            if i not in visited:
                theQueue.append(i)
                visited[i] = current
    if not path:
        return None
    else:
        return path

def bfs_find_pellet(graph, grid, start, goal):
    path = []
    theQueue = collections.deque()
    theQueue.append(start)
    visited = {}
    visited[start] = None
    while theQueue:
        current = theQueue.popleft()
        #stops and returns the best path
        if grid[current[0]][current[1]] == goal:
            findPath(current, visited, path)
            break
        
        #Look for paths
        for i in graph.neighbors(current):
            if i not in visited:
                theQueue.append(i)
                visited[i] = current
    if not path:
        return None
    else:
        return path

def initialize_grid(grid):
    walls = set()
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == I or grid[row][col] == n:
                walls.add((row, col))
    
    new_grid = pacGrid(len(grid), len(grid[0]))
    new_grid.walls = walls
    #print("walls:", walls)
    
    return new_grid
