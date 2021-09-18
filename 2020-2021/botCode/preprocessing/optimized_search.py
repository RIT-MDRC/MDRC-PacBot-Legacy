import math  # inf

from .directions import STOP
from . import lookup_tables  # preprocessed grid (meta)data

def get_dist_and_dir(start, goal):
    # handle this trivial case so the rest of the algorithm can assume that start != goal
    if start == goal:
        return 0, STOP
    
    # if the goal isn't a walkable tile, there's no path
    if goal not in lookup_tables.tile_table:
        return None
    
    # get the tile_table entry for start
    start_entry = lookup_tables.tile_table[start]
    if isinstance(start_entry, int):
        start_locs = ((start_entry, 0, None),)
        start_is_segment = False
    else:
        start_locs = start_entry
        start_is_segment = True
    
    # get the tile_table entry for goal
    goal_entry = lookup_tables.tile_table[goal]
    if isinstance(goal_entry, int):
        goal_locs = ((goal_entry, 0, None),)
        goal_is_segment = False
    else:
        goal_locs = goal_entry
        goal_is_segment = True
    
    # handle some special cases when start & goal are near each other in the graph
    if goal_is_segment:
        if start_is_segment:
            if start_locs[0][0] == goal_locs[0][0] and start_locs[1][0] == goal_locs[1][0]:
                # start & goal are in the same segment
                start_pos = start_locs[0][1]
                goal_pos = goal_locs[0][1]
                if start_pos < goal_pos:
                    return goal_pos - start_pos, start_locs[1][2]
                else:
                    return start_pos - goal_pos, start_locs[0][2]
        elif start_entry == goal_locs[0][0]:
            # start is one of the intersections adjacent to goal's segment
            return goal_locs[0][1], lookup_tables.intersection_table[start_entry][goal_locs[1][0]][2]
        elif start_entry == goal_locs[1][0]:
            # start is one of the intersections adjacent to goal's segment
            return goal_locs[1][1], lookup_tables.intersection_table[start_entry][goal_locs[0][0]][2]
    
    # find the shortest of all combinations of start & goal intersections
    min_dist = math.inf
    for start_iid, start_dist, start_dir in start_locs:
        for goal_iid, goal_dist, _ in goal_locs:
            i2i_dist, i2i_dir, _ = lookup_tables.intersection_table[start_iid][goal_iid]
            total_dist = start_dist + i2i_dist + goal_dist
            if total_dist < min_dist:
                min_dist = total_dist
                min_dist_dir = i2i_dir if start_dir is None else start_dir
    
    return min_dist, min_dist_dir
