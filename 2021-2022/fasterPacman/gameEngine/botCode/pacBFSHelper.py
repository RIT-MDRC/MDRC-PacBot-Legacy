import collections
from functools import lru_cache

from .variables import *

#Used for grid Initialization
class pacGrid: 
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.neighbors = {}
    
    def get_neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0:
            results.reverse() # aesthetics
        # filter out neighbors that are walls
        results = [coords for coords in results if coords not in self.walls]
        return results

def makePathList(node, previousNodes):
    path = []
    while previousNodes[node] is not None:
        path.append(node)
        node = previousNodes[node]
    return path or None

@lru_cache(maxsize=200)
def breadth_first_search(graph, start, goal):
    theQueue = collections.deque()
    theQueue.append(start)
    visited = {}
    visited[start] = None
    while theQueue:
        current = theQueue.popleft()
        #Stops and returns the best path
        if current == goal:
            return makePathList(current, visited)
        
        #Looks for paths
        for i in graph.neighbors[current]:
            if i not in visited:
                theQueue.append(i)
                visited[i] = current
    return None

def bfs_find_pellet(graph, grid, start, goal):
    theQueue = collections.deque()
    theQueue.append(start)
    visited = {}
    visited[start] = None
    while theQueue:
        current = theQueue.popleft()
        #stops and returns the best path
        if grid[current[0]][current[1]] == goal:
            return makePathList(current, visited)
        
        #Look for paths
        for i in graph.neighbors[current]:
            if i not in visited:
                theQueue.append(i)
                visited[i] = current
    return None

def initialize_grid(grid):
    walls = set()
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == I or grid[row][col] == n:
                walls.add((row, col))
    
    new_grid = pacGrid(len(grid), len(grid[0]))
    new_grid.walls = walls
    #print("walls:", walls)
    
    # pre-compute neighbors
    neighbors = {}
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if not (grid[row][col] == I or grid[row][col] == n):
                coords = (row, col)
                neighbors[coords] = tuple(new_grid.get_neighbors(coords))
    new_grid.neighbors = neighbors
    
    return new_grid
