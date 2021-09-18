import string

wall_grid = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 0
    [0,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0],
    [0,1,0,0,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0],
    [0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0],
    [0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0], # 5
    [0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,0,1,0],
    [0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,0,1,0],
    [0,1,0,0,1,1,1,1,0,0,1,2,2,2,2,2,2,2,2,2,0,0,1,1,1,1,0,0,0,1,0],
    [0,1,0,0,1,0,0,1,0,0,1,0,0,2,0,0,0,0,0,2,0,0,1,0,0,1,0,0,0,1,0], # 10
    [0,1,0,0,1,0,0,1,0,0,1,0,0,2,0,0,0,0,0,2,0,0,1,0,0,1,0,0,0,1,0],
    [0,1,1,1,1,0,0,1,1,1,1,0,0,2,0,0,0,0,0,2,2,2,1,0,0,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,1,0,0,0,0,0],
    [0,1,1,1,1,0,0,1,1,1,1,0,0,2,0,0,0,0,0,2,2,2,1,0,0,1,1,1,1,1,0], # 15
    [0,1,0,0,1,0,0,1,0,0,1,0,0,2,0,0,0,0,0,2,0,0,1,0,0,1,0,0,0,1,0],
    [0,1,0,0,1,0,0,1,0,0,1,0,0,2,0,0,0,0,0,2,0,0,1,0,0,1,0,0,0,1,0],
    [0,1,0,0,1,1,1,1,0,0,1,2,2,2,2,2,2,2,2,2,0,0,1,1,1,1,0,0,0,1,0],
    [0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,0,1,0],
    [0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,0,1,0], # 20
    [0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0],
    [0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0],
    [0,1,0,0,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0],
    [0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0], # 25
    [0,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
#    |         |         |         |         |         |         |
#    0         5        10        15       20         25       30

wall_grid = [
    [cell == 0 for cell in row]
    for row in wall_grid
]

# find neighbors and intersection locations
neighbors = {}
intersections = []
r_range = range(len(wall_grid))
c_range = range(len(wall_grid[0]))
for r in r_range:
    for c in c_range:
        if wall_grid[r][c]:
            continue
        ns = []
        for r2, c2 in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
            if r2 in r_range and c2 in c_range and not wall_grid[r2][c2]:
                ns.append((r2, c2))
        neighbors[(r, c)] = tuple(ns)
        if len(ns) > 2:
            intersections.append((r, c))
intersections = tuple(intersections)

# find segments
segment_grid = {}
def get_segment_intersections(loc, state=None):
    if state is None:
        state = [], set()
    try:
        int_id = intersections.index(loc)
        state[0].append(int_id)
    except ValueError:
        state[1].add(loc)
        for loc2 in neighbors[loc]:
            if loc2 not in state[1]:
                get_segment_intersections(loc2, state)
    state[0].sort()
    return tuple(state[0])
def flood_fill(loc, fill_value):
    segment_grid[loc] = fill_value
    for loc2 in neighbors[loc]:
        if loc2 not in intersections and loc2 not in segment_grid:
            flood_fill(loc2, fill_value)
cur_seg_id = 0
for loc in neighbors.keys():
    if loc not in segment_grid:
        try:
            segment_grid[loc] = intersections.index(loc)
        except ValueError:
            flood_fill(loc, get_segment_intersections(loc))
            cur_seg_id += 1

# print the results
for r in r_range:
    row_str = ''
    for c in c_range:
        loc = (r, c)
        if wall_grid[r][c]:
            row_str += '  '
        elif loc in intersections:
            row_str += '[]'
        else:
            si1, si2 = segment_grid[loc]
            row_str += string.ascii_letters[si1 % len(string.ascii_letters)]
            row_str += string.ascii_letters[si2 % len(string.ascii_letters)]
    print(row_str)

print(len(intersections), 'intersections')
print(cur_seg_id, 'segments')
print(len(neighbors), 'total walkable tiles')

# print()
# print('intersection_locations =', repr(intersections).replace(' ', ''))
# print('segment_grid =', repr(segment_grid).replace(' ', ''))


print()

from collections import deque
def makePathList(node, previousNodes):
    path = []
    while previousNodes[node] is not None:
        path.append(node)
        node = previousNodes[node]
    return path or None
def breadth_first_search(start, goal, allow_intersections=True):
    nodeQueue = deque()
    nodeQueue.append(start)
    visited = {start: None}
    
    visit_count = 0
    try:
        while nodeQueue:
            current = nodeQueue.popleft()
            visit_count += 1
            #Stops and returns the best path
            if current == goal:
                return makePathList(current, visited)
            if not allow_intersections and len(neighbors[current]) > 2:
                continue
            
            #Looks for paths
            for n in neighbors[current]:
                if n not in visited:
                    nodeQueue.append(n)
                    visited[n] = current
    finally:
        pass #print(f'BFS visited {visit_count} nodes')
    return None

from directions import *

# compute tile_table
tile_table = {}
for loc in neighbors.keys(): # loop over all walkable locations
    try:
        # if it's an intersection, the entry is the intersection index
        tile_table[loc] = intersections.index(loc)
    except ValueError:
        # it's not an intersection - the entry is info about paths to the two adjacent intersections
        entry = []
        for iid in segment_grid[loc]:
            i_loc = intersections[iid]
            path = breadth_first_search(loc, i_loc, allow_intersections=False)
            entry.append((iid, len(path), get_direction(loc, path[-1])))
        tile_table[loc] = tuple(entry)

# compute intersection_table
def get_segment_dir(loc1, iid2):
    for n in neighbors[loc1]:
        if any(iid == iid2 for iid,_,_ in tile_table[n]):
            return get_direction(loc1, n)
intersection_table = [[None]*len(intersections) for _ in range(len(intersections))]
for i in range(len(intersections)):
    loc_i = intersections[i]
    intersection_table[i][i] = (0, STOP, STOP)
    for j in range(i+1, len(intersections)):
        loc_j = intersections[j]
        
        path = breadth_first_search(intersections[i], intersections[j])
        path_len = len(path)
        dir_i = get_direction(loc_i, path[-1])
        dir_j = get_direction(loc_j, path[1])
        
        intersection_table[i][j] = (path_len, dir_i, get_segment_dir(loc_i, j))
        intersection_table[j][i] = (path_len, dir_j, get_segment_dir(loc_j, i))
intersection_table = tuple(tuple(x) for x in intersection_table)

with open('lookup_tables.py', 'w') as f:
    f.write('intersection_table = ' + repr(intersection_table).replace(' ', '') + '\n')
    f.write('tile_table = ' + repr(tile_table).replace(' ', '') + '\n')

# print('neighbors =', repr(neighbors).replace(' ', ''))
