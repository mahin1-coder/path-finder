# enhanced_astar.py - improved A* pathfinding with two extra cost penalties:
#   1. Turn penalty  - discourages sharp direction changes
#   2. Proximity penalty - discourages moving close to walls

import heapq, time
from utils import Node, get_neighbors, heuristic, move_cost, reconstruct_path


# Penalty for turning sharply. Uses cosine of angle between incoming/outgoing
# direction vectors. Straight = 0 penalty, U-turn = full alpha penalty.
def turn_penalty(parent, current, neighbor, alpha=0.5):
    if parent is None:
        return 0.0
    d_in  = (current[0]-parent[0],   current[1]-parent[1])
    d_out = (neighbor[0]-current[0], neighbor[1]-current[1])
    dot = d_in[0]*d_out[0] + d_in[1]*d_out[1]
    mag = ((d_in[0]**2+d_in[1]**2)**0.5) * ((d_out[0]**2+d_out[1]**2)**0.5)
    if mag == 0:
        return 0.0
    cos_a = max(-1.0, min(1.0, dot/mag))
    return alpha * (1.0 - cos_a) / 2.0  # 0 when straight, alpha when reversed


# Penalty for being close to obstacles. Nearby walls add beta/distance cost.
def proximity_penalty(grid, pos, radius=2, beta=0.4):
    rows, cols = grid.shape
    r, c = pos
    penalty = 0.0
    for dr in range(-radius, radius+1):
        for dc in range(-radius, radius+1):
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                dist = (dr**2 + dc**2) ** 0.5
                if dist > 0:
                    penalty += beta / dist
    return penalty


def enhanced_astar(grid, start, goal, alpha=0.5, beta=0.4, radius=2):
    t0 = time.perf_counter()

    start_node = Node(start)
    start_node.h = heuristic(start, goal)
    start_node.f = start_node.h

    open_list = []
    heapq.heappush(open_list, start_node)

    best_g = {start: 0.0}
    closed = set()
    expanded = 0

    while open_list:
        current = heapq.heappop(open_list)

        if current.position in closed:
            continue

        closed.add(current.position)
        expanded += 1

        if current.position == goal:
            return reconstruct_path(current), expanded, time.perf_counter()-t0, closed

        parent_pos = current.parent.position if current.parent else None

        for nb in get_neighbors(grid, current.position):
            if nb in closed:
                continue

            # base cost + turn penalty + wall proximity penalty
            g_new = current.g + move_cost(current.position, nb)
            g_new += turn_penalty(parent_pos, current.position, nb, alpha)
            g_new += proximity_penalty(grid, nb, radius, beta)

            if g_new < best_g.get(nb, float('inf')):
                best_g[nb] = g_new
                node = Node(nb, current)
                node.g = g_new
                node.h = heuristic(nb, goal)
                node.f = node.g + node.h
                heapq.heappush(open_list, node)

    return None, expanded, time.perf_counter()-t0, closed
