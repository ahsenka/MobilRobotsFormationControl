import matplotlib.pyplot as plt


def draw_grid(grid, leader, goal, path=None):
    plt.clf()

    for x in range(grid.width):
        for y in range(grid.height):
            plt.scatter(x, y, marker="s", s=300, edgecolors="black")

    if path:
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        plt.plot(path_x, path_y, linewidth=2, label="A* Path")

    obstacle_x = [p[0] for p in grid.obstacles]
    obstacle_y = [p[1] for p in grid.obstacles]
    if grid.obstacles:
        plt.scatter(obstacle_x, obstacle_y, marker="s", s=300, label="Obstacle")

    plt.scatter(leader.position[0], leader.position[1], s=500, label="Leader")
    plt.scatter(goal[0], goal[1], s=500, marker="*", label="Goal")

    plt.xlim(-1, grid.width)
    plt.ylim(-1, grid.height)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.grid(True)
    plt.legend(loc="upper right")
    plt.pause(0.3)

def draw_grid(grid, leader, followers, goal, path=None):
    import matplotlib.pyplot as plt

    plt.clf()

    for x in range(grid.width):
        for y in range(grid.height):
            plt.scatter(x, y, marker="s", s=300, edgecolors="black")

    if path:
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        plt.plot(path_x, path_y, linewidth=2)

    # obstacles
    if grid.obstacles:
        ox = [p[0] for p in grid.obstacles]
        oy = [p[1] for p in grid.obstacles]
        plt.scatter(ox, oy, marker="s", s=300)

    # leader
    plt.scatter(leader.position[0], leader.position[1], s=500, label="Leader")

    # followers
    for f in followers:
        plt.scatter(f.position[0], f.position[1], s=500, label="Follower")

    # goal
    plt.scatter(goal[0], goal[1], s=500, marker="*", label="Goal")

    plt.xlim(-1, grid.width)
    plt.ylim(-1, grid.height)
    plt.gca().set_aspect("equal")
    plt.grid(True)
    plt.pause(0.3)