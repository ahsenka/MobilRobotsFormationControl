from environment.grid import Grid
from algorithms.astar import astar
from agents.leader import Leader
from agents.follower import Follower
from formation.triangle import get_triangle_offsets
from utils.visualization import draw_grid
import matplotlib.pyplot as plt


def main():
    grid = Grid(10, 10)

    grid.obstacles = {
        (3, 0), (3, 1), (3, 2), (3, 3),
        (3, 4), (3, 5)
    }

    start = (0, 0)
    goal = (7, 7)

    leader = Leader(start)

    path = astar(grid, start, goal)
    leader.set_path(path.copy())

    offsets = get_triangle_offsets()

    followers = [
        Follower(start, offsets[1]),
        Follower(start, offsets[2]),
        Follower(start, offsets[3]),
    ]

    plt.ion()

    while leader.path:
        leader.move()

        for f in followers:
            f.move(leader.position)

        draw_grid(grid, leader, followers, goal, path)

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()