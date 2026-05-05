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
    (6, 2), (6, 3), (6, 4), (6, 5),
    (6, 6)
    }

    start = (4, 4)
    goal = (8, 8)

    leader = Leader(start)

    path = astar(grid, start, goal)
    if not path:
        print("Hedefe giden yol bulunamadı. Engel veya başlangıç/hedef konumlarını kontrol et.")
        return
    leader.set_path(path.copy())

    offsets = get_triangle_offsets()

    followers = [
    Follower((start[0] + offsets[1][0], start[1] + offsets[1][1]), offsets[1]),
    Follower((start[0] + offsets[2][0], start[1] + offsets[2][1]), offsets[2]),
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