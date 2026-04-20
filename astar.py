# astar.py - standard A* pathfinding

import heapq, time
from utils import Node, get_neighbors, heuristic, move_cost, reconstruct_path


def astar(grid, start, goal):
    t0 = time.perf_counter()

    # set up the start node
    start_node = Node(start)
    start_node.h = heuristic(start, goal)
    start_node.f = start_node.h

    open_list = []
    heapq.heappush(open_list, start_node)

    best_g = {start: 0.0}   # cheapest cost seen so far to each position
    closed = set()           # positions already fully processed
    expanded = 0

    while open_list:
        current = heapq.heappop(open_list)

        if current.position in closed:
            continue  # skip duplicate entries in the heap

        closed.add(current.position)
        expanded += 1

        # reached the goal - trace path back and return
        if current.position == goal:
            return reconstruct_path(current), expanded, time.perf_counter()-t0, closed

        for nb in get_neighbors(grid, current.position):
            if nb in closed:
                continue
            g_new = current.g + move_cost(current.position, nb)
            if g_new < best_g.get(nb, float('inf')):
                best_g[nb] = g_new
                node = Node(nb, current)
                node.g = g_new
                node.h = heuristic(nb, goal)
                node.f = node.g + node.h
                heapq.heappush(open_list, node)

    return None, expanded, time.perf_counter()-t0, closed  # no path found
