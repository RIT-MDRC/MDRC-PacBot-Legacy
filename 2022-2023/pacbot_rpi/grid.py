from bot_math import Position

W = True  # wall
U = True  # unreachable, basically wall
o = False  # open

GRID = [[W, W, W, W, W, W, W, W, W, W, W, W, U, U, U, U, U, U, U, U, U, W, W, W, W, W, W, W, W, W, W][::-1],  # 0
        [W, o, o, o, o, W, W, o, o, o, o, W, U, U, U, U, U, U, U, U, U, W, o, o, o, o, o, o, o, o, W][::-1],
        [W, o, W, W, o, W, W, o, W, W, o, W, U, U, U, U, U, U, U, U, U, W, o, W, W, o, W, W, W, o, W][::-1],
        [W, o, W, W, o, o, o, o, W, W, o, W, U, U, U, U, U, U, U, U, U, W, o, W, W, o, W, U, W, o, W][::-1],
        [W, o, W, W, o, W, W, W, W, W, o, W, U, U, U, U, U, U, U, U, U, W, o, W, W, o, W, U, W, o, W][::-1],
        [W, o, W, W, o, W, W, W, W, W, o, W, W, W, W, W, W, W, W, W, W, W, o, W, W, o, W, W, W, o, W][::-1],  # 5
        [W, o, W, W, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, W][::-1],
        [W, o, W, W, W, W, W, o, W, W, o, W, W, W, W, W, o, W, W, W, W, W, W, W, W, o, W, W, W, o, W][::-1],
        [W, o, W, W, W, W, W, o, W, W, o, W, W, W, W, W, o, W, W, W, W, W, W, W, W, o, W, U, W, o, W][::-1],
        [W, o, W, W, o, o, o, o, W, W, o, o, o, o, o, o, o, o, o, o, W, W, o, o, o, o, W, U, W, o, W][::-1],
        [W, o, W, W, o, W, W, o, W, W, o, W, W, o, W, W, W, W, W, o, W, W, o, W, W, o, W, U, W, o, W][::-1],  # 10
        [W, o, W, W, o, W, W, o, W, W, o, W, W, o, W, W, W, W, W, o, W, W, o, W, W, o, W, W, W, o, W][::-1],
        [W, o, o, o, o, W, W, o, o, o, o, W, W, o, W, W, W, W, W, o, o, o, o, W, W, o, o, o, o, o, W][::-1],
        [W, o, W, W, W, W, W, o, W, W, W, W, W, o, W, W, W, W, W, o, W, W, W, W, W, o, W, W, W, W, W][::-1],
        [W, o, W, W, W, W, W, o, W, W, W, W, W, o, W, W, W, W, W, o, W, W, W, W, W, o, W, W, W, W, W][::-1],
        [W, o, o, o, o, W, W, o, o, o, o, W, W, o, W, W, W, W, W, o, o, o, o, W, W, o, o, o, o, o, W][::-1],  # 15
        [W, o, W, W, o, W, W, o, W, W, o, W, W, o, W, W, W, W, W, o, W, W, o, W, W, o, W, W, W, o, W][::-1],
        [W, o, W, W, o, W, W, o, W, W, o, W, W, o, W, W, W, W, W, o, W, W, o, W, W, o, W, U, W, o, W][::-1],
        [W, o, W, W, o, o, o, o, W, W, o, o, o, o, o, o, o, o, o, o, W, W, o, o, o, o, W, U, W, o, W][::-1],
        [W, o, W, W, W, W, W, o, W, W, o, W, W, W, W, W, o, W, W, W, W, W, W, W, W, o, W, U, W, o, W][::-1],
        [W, o, W, W, W, W, W, o, W, W, o, W, W, W, W, W, o, W, W, W, W, W, W, W, W, o, W, W, W, o, W][::-1],  # 20
        [W, o, W, W, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, o, W][::-1],
        [W, o, W, W, o, W, W, W, W, W, o, W, W, W, W, W, W, W, W, W, W, W, o, W, W, o, W, W, W, o, W][::-1],
        [W, o, W, W, o, W, W, W, W, W, o, W, U, U, U, U, U, U, U, U, U, W, o, W, W, o, W, U, W, o, W][::-1],
        [W, o, W, W, o, o, o, o, W, W, o, W, U, U, U, U, U, U, U, U, U, W, o, W, W, o, W, U, W, o, W][::-1],
        [W, o, W, W, o, W, W, o, W, W, o, W, U, U, U, U, U, U, U, U, U, W, o, W, W, o, W, W, W, o, W][::-1],  # 25
        [W, o, o, o, o, W, W, o, o, o, o, W, U, U, U, U, U, U, U, U, U, W, o, o, o, o, o, o, o, o, W][::-1],
        [W, W, W, W, W, W, W, W, W, W, W, W, U, U, U, U, U, U, U, U, U, W, W, W, W, W, W, W, W, W, W][::-1]]
#        |         |         |         |         |         |         |
#        0         5        10        15       20         25       30

GRID_WIDTH = len(GRID)
GRID_HEIGHT = len(GRID[0])


def space_is_open(pos: Position) -> bool:
    return GRID[round(pos.y)][round(pos.x)]


GRID_OPEN_SPACES = []
for x in range(GRID_WIDTH):
    for y in range(GRID_HEIGHT):
        if GRID[x][y] == o:
            GRID_OPEN_SPACES.append(Position(x, y))


def get_grid_open_spaces():
    return GRID_OPEN_SPACES


def grid_bfs_path(start: Position, target: Position):
    if start == target:
        return [target]

    # represents the visited nodes
    bfs_nodes: list[tuple[int, Position]] = [(-1, start)]
    # represent the index where all indices <= this index were added in the last iteration
    last_added_indices = 0

    while 1:
        # represents the length of bfs_nodes before this iteration starts, which will be last_added_indices in the next
        # iteration
        new_last_added_indices = len(bfs_nodes)
        # add new nodes to list

        # for each possible change in position
        for pose_change in [
            [1, 0],
            [-1, 0],
            [0, 1],
            [0, -1]
        ]:
            # for each visited position that was added in the last iteration
            for pos_i in range(last_added_indices, len(bfs_nodes)):
                prev_i, pos = bfs_nodes[pos_i]
                new_pos = Position(pos.x + pose_change[0], pos.y + pose_change[1])

                # if the new space is not a valid position, don't include it
                if new_pos not in get_grid_open_spaces():
                    continue

                # if the new space is the target, we are done
                if new_pos == target:
                    # construct the path by tracing the nodes that led us here
                    path = [pos, new_pos]
                    # while we aren't at the start node
                    while prev_i >= 0:
                        path = [bfs_nodes[prev_i][1]] + path
                        prev_i = bfs_nodes[prev_i][0]
                    # clean up path by removing points that aren't at turning points
                    new_path = [path[0]]
                    direction = [path[1].x - path[0].x, path[1].y - path[0].y]
                    for i in range(2, len(path)):
                        new_direction = [path[i].x - path[i - 1].x,
                                         path[i].y - path[i - 1].y]
                        if new_direction != direction:
                            new_path.append(path[i - 1])
                            direction = new_direction
                    return new_path

                # don't add this position if we have already visited it
                already_found = False
                for prev_i, bfs_pose in bfs_nodes:
                    if bfs_pose == new_pos:
                        already_found = True
                        break

                if not already_found:
                    bfs_nodes.append((pos_i, new_pos))
        # if we didn't go anywhere new last iteration, return no path
        # this should never happen
        if new_last_added_indices == len(bfs_nodes):
            return []

        # for the next iteration, only consider nodes that were added in this iteration
        last_added_indices = new_last_added_indices
