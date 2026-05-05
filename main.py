from environment.grid import Grid
from algorithms.astar import astar
from agents.leader import Leader
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

    print("A* Path:", path)

    plt.ion()

    while leader.path:
        leader.move()
        draw_grid(grid, leader, goal, path)

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()