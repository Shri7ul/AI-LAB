# Name: Shriful Islam
# ID: 0112410115
# Heuristic: Manhattan distance is admissible because movement is limited
# to four directions and every move costs at least 1.

import heapq


def astar(grid: list[str], start: tuple[int, int], goal: tuple[int, int]) -> tuple[list[tuple[int, int]], int]:

    # Manhattan distance is admissible because movement is only
    # up/down/left/right, and every move costs at least 1.
    # Therefore, Manhattan distance never overestimates the true
    # minimum remaining cost to reach the goal.
    def heuristic(cell):
        r, c = cell
        gr, gc = goal
        return abs(r - gr) + abs(c - gc)

    rows = len(grid)
    cols = len(grid[0])

    pq = []

    g_score = {start: 0}

    came_from = {}

    h = heuristic(start)
    heapq.heappush(pq, (h, 0, start))

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while pq:
        f, current_g, current = heapq.heappop(pq)

        # Ignore outdated entries in the priority queue.
        if current_g != g_score.get(current):
            continue

        if current == goal:
            path = []
            node = goal

            while node != start:
                path.append(node)
                node = came_from[node]

            path.append(start)
            path.reverse()

            return path, current_g

        r, c = current

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            if grid[nr][nc] == '#':
                continue

            neighbor = (nr, nc)

            if grid[nr][nc] == '~':
                move_cost = 3
            else:
                move_cost = 1

            new_g = current_g + move_cost

            if new_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = new_g
                came_from[neighbor] = current

                h = heuristic(neighbor)
                f = new_g + h

                heapq.heappush(pq, (f, new_g, neighbor))

    return [], -1


grid = [
    "S..#....",
    ".##.~~..",
    "....~.#.",
    "..#..#..",
    "....#..G",
]

start = (0, 0)
goal = (4, 7)

path, cost = astar(grid, start, goal)

print("Cost:", cost)
print("Path:", path)