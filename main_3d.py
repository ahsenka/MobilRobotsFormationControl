from environment.grid3d import Grid3D
from algorithms.astar3d import astar_3d
from formation.formations3d import get_triangle_3d_offsets, get_tetrahedron_offsets
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


class Robot3D:
    def __init__(self, robot_id, position, offset=(0, 0, 0)):
        self.robot_id = robot_id
        self.position = position
        self.offset = offset

    def target_position(self, leader_position):
        return (
            leader_position[0] + self.offset[0],
            leader_position[1] + self.offset[1],
            leader_position[2] + self.offset[2],
        )

    def move_towards_target(self, leader_position):
        target = self.target_position(leader_position)

        x, y, z = self.position
        tx, ty, tz = target

        dx = tx - x
        dy = ty - y
        dz = tz - z

        if abs(dx) >= abs(dy) and abs(dx) >= abs(dz) and dx != 0:
            x += 1 if dx > 0 else -1
        elif abs(dy) >= abs(dx) and abs(dy) >= abs(dz) and dy != 0:
            y += 1 if dy > 0 else -1
        elif dz != 0:
            z += 1 if dz > 0 else -1

        self.position = (x, y, z)


def draw_3d_frame(ax, grid, leader, followers, goal, path, title):
    ax.clear()

    if path:
        px = [p[0] for p in path]
        py = [p[1] for p in path]
        pz = [p[2] for p in path]
        ax.plot(px, py, pz, linewidth=2, label="A* Path")

    if grid.obstacles:
        ox = [p[0] for p in grid.obstacles]
        oy = [p[1] for p in grid.obstacles]
        oz = [p[2] for p in grid.obstacles]
        ax.scatter(ox, oy, oz, marker="s", s=80, label="Obstacles")

    ax.scatter(
        leader.position[0],
        leader.position[1],
        leader.position[2],
        s=150,
        label="Leader"
    )

    for follower in followers:
        ax.scatter(
            follower.position[0],
            follower.position[1],
            follower.position[2],
            s=120,
            label=follower.robot_id
        )

    # Formation connection lines
    all_robots = [leader] + followers
    for i in range(len(all_robots)):
        for j in range(i + 1, len(all_robots)):
            p1 = all_robots[i].position
            p2 = all_robots[j].position
            ax.plot(
                [p1[0], p2[0]],
                [p1[1], p2[1]],
                [p1[2], p2[2]],
                linestyle="--",
                linewidth=1
            )

    ax.scatter(goal[0], goal[1], goal[2], marker="*", s=200, label="Goal")

    ax.set_title(title)
    ax.set_xlim(0, grid.width)
    ax.set_ylim(0, grid.height)
    ax.set_zlim(0, grid.depth)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.legend(loc="upper left")


def run_3d_simulation(formation_name, offsets, output_file):
    grid = Grid3D(25, 25, 15)

    grid.obstacles = {
        (10, 8, 5), (10, 9, 5), (10, 10, 5),
        (12, 12, 6), (12, 13, 6), (12, 14, 6),
        (15, 15, 8), (15, 16, 8), (15, 17, 8),
    }

    start = (4, 4, 4)
    goal = (20, 20, 10)

    path = astar_3d(grid, start, goal)

    if not path:
        print(f"{formation_name}: Hedefe giden yol bulunamadı.")
        return

    leader = Robot3D("Leader", start, offsets[0])

    followers = []

    for index, offset in enumerate(offsets[1:], start=1):
        start_position = (
            start[0] + offset[0],
            start[1] + offset[1],
            start[2] + offset[2],
        )

        followers.append(
            Robot3D(
                f"Follower {index}",
                start_position,
                offset
            )
        )

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    path_copy = path.copy()

    def update(frame):
        if path_copy:
            leader.position = path_copy.pop(0)

            for follower in followers:
                follower.move_towards_target(leader.position)

        draw_3d_frame(
            ax,
            grid,
            leader,
            followers,
            goal,
            path,
            f"3D {formation_name} Formation"
        )

    anim = FuncAnimation(
        fig,
        update,
        frames=len(path) + 15,
        interval=300,
        repeat=False
    )

    anim.save(output_file, writer=PillowWriter(fps=3))
    plt.close()

    print(f"{output_file} oluşturuldu.")


def main():
    run_3d_simulation(
        "Triangle",
        get_triangle_3d_offsets(),
        "simulation_3d_triangle.gif"
    )

    run_3d_simulation(
        "Tetrahedron",
        get_tetrahedron_offsets(),
        "simulation_3d_tetrahedron.gif"
    )


if __name__ == "__main__":
    main()