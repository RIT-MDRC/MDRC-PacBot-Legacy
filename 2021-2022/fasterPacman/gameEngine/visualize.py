#!/usr/bin/env python3

import os, sys
from graphics import Visualizer
from graphics.variables import Split

ADDRESS = "localhost"
PORT = os.environ.get("SERVER_PORT", 11297)

class Visualize:
    def __init__(self):
        walls = ('-w' in sys.argv or os.environ.get("WALLS",False))
        walls = True
        pacman = ('-p' in sys.argv or os.environ.get("PACMAN",False))
        pacman = True
        top = ('-t' in sys.argv or os.environ.get("TOP",False))
        # top = True
        bottom = ('-b' in sys.argv or os.environ.get("BOTTOM",False))
        # bottom = True
        split = Split.FULL
        if top:
            split = Split.TOP
        elif bottom:
            split = Split.BOTTOM
        self.visualizer = Visualizer(ADDRESS, PORT, walls, pacman, split)
        self.visualizer.run()

# if __name__ == "__main__":
#     main()
