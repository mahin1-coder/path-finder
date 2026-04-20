# utils.py - helper functions shared by both algorithms

import numpy as np


# Node stores position, parent (for tracing the path back), and g/h/f scores
class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0.0   # cost from start to here
        self.h = 0.0   # estimated cost from here to goal
        self.f = 0.0   # total = g + h

    def __lt__(self, other):   # needed so heapq can compare nodes
        return self.f < other.f


# Returns all walkable neighbors (8 directions)
def get_neighbors(grid, pos):
    rows, cols = grid.shape
    r, c = pos
    dirs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    return [(r+dr, c+dc) for dr,dc in dirs
            if 0 <= r+dr < rows and 0 <= c+dc < cols
            and grid[r+dr][c+dc] == 0]


# Diagonal moves cost sqrt(2), straight moves cost 1
def move_cost(a, b):
    return 1.414 if abs(a[0]-b[0]) == 1 and abs(a[1]-b[1]) == 1 else 1.0


# Octile distance heuristic (works well for 8-direction grids)
def heuristic(pos, goal):
    dr, dc = abs(pos[0]-goal[0]), abs(pos[1]-goal[1])
    return max(dr, dc) + 0.414 * min(dr, dc)


# Walk parent pointers back from goal to start
def reconstruct_path(node):
    path = []
    while node:
        path.append(node.position)
        node = node.parent
    return path[::-1]


# Total Euclidean length of a path
def path_length(path):
    total = 0.0
    for i in range(1, len(path)):
        dr = path[i][0] - path[i-1][0]
        dc = path[i][1] - path[i-1][1]
        total += (dr**2 + dc**2) ** 0.5
    return total


# --- Test maps ---

def make_map1():
    grid = np.zeros((20, 20), dtype=np.int8)
    for pos in [(5,5),(5,6),(5,7),(5,8),(5,9),(10,10),(10,11),(10,12),
                (3,14),(4,14),(5,14),(6,14),(15,3),(15,4),(15,5),(16,5),(17,5),
                (8,3),(9,3),(10,3)]:
        grid[pos] = 1
    return grid, (1,1), (18,18), "Map 1 - Open Field"


def make_map2():
    grid = np.zeros((20, 20), dtype=np.int8)
    for c in list(range(0,9)) + list(range(11,20)):  # wall with gap at col 10
        grid[10][c] = 1
    for pos in [(5,5),(6,5),(7,5),(8,5),(3,15),(4,15),(5,15),(6,15),
                (14,3),(14,4),(14,5),(14,6),(14,14),(14,15),(14,16),(14,17)]:
        grid[pos] = 1
    return grid, (1,1), (18,18), "Map 2 - Narrow Corridor"


def make_map3():
    grid = np.zeros((25, 25), dtype=np.int8)
    rng = np.random.default_rng(seed=42)  # fixed seed so results are repeatable
    safe = {(0,0),(0,1),(1,0),(24,24),(23,24),(24,23)}
    for r in range(25):
        for c in range(25):
            if (r,c) not in safe and rng.random() < 0.25:
                grid[r][c] = 1
    return grid, (0,0), (24,24), "Map 3 - Dense Clutter"


ALL_MAPS = [make_map1, make_map2, make_map3]
