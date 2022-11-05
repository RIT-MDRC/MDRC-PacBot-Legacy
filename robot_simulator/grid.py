W = True   # wall
U = True   # unreachable, basically wall
o = False  # open

GRID = [[W,W,W,W,W,W,W,W,W,W,W,W,U,U,U,U,U,U,U,U,U,W,W,W,W,W,W,W,W,W,W][::-1], # 0
        [W,o,o,o,o,W,W,o,o,o,o,W,U,U,U,U,U,U,U,U,U,W,o,o,o,o,o,o,o,o,W][::-1],
        [W,o,W,W,o,W,W,o,W,W,o,W,U,U,U,U,U,U,U,U,U,W,o,W,W,o,W,W,W,o,W][::-1],
        [W,o,W,W,o,o,o,o,W,W,o,W,U,U,U,U,U,U,U,U,U,W,o,W,W,o,W,U,W,o,W][::-1],
        [W,o,W,W,o,W,W,W,W,W,o,W,U,U,U,U,U,U,U,U,U,W,o,W,W,o,W,U,W,o,W][::-1],
        [W,o,W,W,o,W,W,W,W,W,o,W,W,W,W,W,W,W,W,W,W,W,o,W,W,o,W,W,W,o,W][::-1], # 5
        [W,o,W,W,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,W][::-1],
        [W,o,W,W,W,W,W,o,W,W,o,W,W,W,W,W,o,W,W,W,W,W,W,W,W,o,W,W,W,o,W][::-1],
        [W,o,W,W,W,W,W,o,W,W,o,W,W,W,W,W,o,W,W,W,W,W,W,W,W,o,W,U,W,o,W][::-1],
        [W,o,W,W,o,o,o,o,W,W,o,o,o,o,o,o,o,o,o,o,W,W,o,o,o,o,W,U,W,o,W][::-1],
        [W,o,W,W,o,W,W,o,W,W,o,W,W,o,W,W,W,W,W,o,W,W,o,W,W,o,W,U,W,o,W][::-1], # 10
        [W,o,W,W,o,W,W,o,W,W,o,W,W,o,W,W,W,W,W,o,W,W,o,W,W,o,W,W,W,o,W][::-1],
        [W,o,o,o,o,W,W,o,o,o,o,W,W,o,W,W,W,W,W,o,o,o,o,W,W,o,o,o,o,o,W][::-1],
        [W,o,W,W,W,W,W,o,W,W,W,W,W,o,W,W,W,W,W,o,W,W,W,W,W,o,W,W,W,W,W][::-1],
        [W,o,W,W,W,W,W,o,W,W,W,W,W,o,W,W,W,W,W,o,W,W,W,W,W,o,W,W,W,W,W][::-1],
        [W,o,o,o,o,W,W,o,o,o,o,W,W,o,W,W,W,W,W,o,o,o,o,W,W,o,o,o,o,o,W][::-1], # 15
        [W,o,W,W,o,W,W,o,W,W,o,W,W,o,W,W,W,W,W,o,W,W,o,W,W,o,W,W,W,o,W][::-1],
        [W,o,W,W,o,W,W,o,W,W,o,W,W,o,W,W,W,W,W,o,W,W,o,W,W,o,W,U,W,o,W][::-1],
        [W,o,W,W,o,o,o,o,W,W,o,o,o,o,o,o,o,o,o,o,W,W,o,o,o,o,W,U,W,o,W][::-1],
        [W,o,W,W,W,W,W,o,W,W,o,W,W,W,W,W,o,W,W,W,W,W,W,W,W,o,W,U,W,o,W][::-1],
        [W,o,W,W,W,W,W,o,W,W,o,W,W,W,W,W,o,W,W,W,W,W,W,W,W,o,W,W,W,o,W][::-1], # 20
        [W,o,W,W,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,W][::-1],
        [W,o,W,W,o,W,W,W,W,W,o,W,W,W,W,W,W,W,W,W,W,W,o,W,W,o,W,W,W,o,W][::-1],
        [W,o,W,W,o,W,W,W,W,W,o,W,U,U,U,U,U,U,U,U,U,W,o,W,W,o,W,U,W,o,W][::-1],
        [W,o,W,W,o,o,o,o,W,W,o,W,U,U,U,U,U,U,U,U,U,W,o,W,W,o,W,U,W,o,W][::-1],
        [W,o,W,W,o,W,W,o,W,W,o,W,U,U,U,U,U,U,U,U,U,W,o,W,W,o,W,W,W,o,W][::-1], # 25
        [W,o,o,o,o,W,W,o,o,o,o,W,U,U,U,U,U,U,U,U,U,W,o,o,o,o,o,o,o,o,W][::-1],
        [W,W,W,W,W,W,W,W,W,W,W,W,U,U,U,U,U,U,U,U,U,W,W,W,W,W,W,W,W,W,W][::-1]]
#        |         |         |         |         |         |         |
#        0         5        10        15       20         25       30

GRID_WIDTH = len(GRID)
GRID_HEIGHT = len(GRID[0])
