import heapq


def heuristic_3d(a, b):
    return (
        abs(a[0] - b[0]) +
        abs(a[1] - b[1]) +
        abs(a[2] - b[2])
    )


def astar_3d(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {start: None}
    cost_so_far = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            break

        for neighbor in grid.neighbors(current):
            new_cost = cost_so_far[current] + 1

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic_3d(neighbor, goal)
                heapq.heappush(open_set, (priority, neighbor))
                came_from[neighbor] = current

    if goal not in came_from:
        return []

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path