STOP = 0
UP = 1     # +Y
DOWN = 2   # -Y
RIGHT = 3  # +X
LEFT = 4   # -X

def get_direction(loc1, loc2):
    if loc1 == loc2:
        return STOP
    x1, y1 = loc1
    x2, y2 = loc2
    if x2 > x1:
        return RIGHT
    elif x2 < x1:
        return LEFT
    elif y2 > y1:
        return UP
    elif y2 < y1:
        return DOWN
    raise ValueError("locations are the same")

def move_direction(loc, direction):
    if direction == STOP:
        return loc
    x, y = loc
    if direction == RIGHT:
        return (x+1, y)
    elif direction == LEFT:
        return (x-1, y)
    elif direction == UP:
        return (x, y+1)
    elif direction == DOWN:
        return (x, y-1)
    raise ValueError("invalid direction")
