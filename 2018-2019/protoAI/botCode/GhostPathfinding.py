#!/usr/bin/env python3
import queue as Queue




def getDirection(grid, ghost, pacman):
    path = getPath(grid, ghost, pacman)
    return directionOfPath(path), lengthOfPath(path) 


def getPath(grid, ghost, pacman):
    queue = Queue.Queue()
    queue.put([ghost])

    while queue.not_empty:
        path = queue.get()

        node = path[-1]

        if node == ghost:
            return path
        
        for adjacent in grid[node.]
    
    return 0


def lengthOfPath(path):
    return 0


def directionOfPath(path):
    return 0


def gridToGraph(grid):

    return 0
