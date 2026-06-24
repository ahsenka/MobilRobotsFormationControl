from environment.grid3d import Grid3D
from algorithms.astar3d import astar_3d
from agents.follower_3d import Follower3D
from communication.communication_bus_3d import CommunicationBus3D
from formation.formations3d import get_triangle_3d_offsets, get_tetrahedron_offsets
from training_3d import train_3d_followers

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


class Leader3D:
    def __init__(self, start_pos):
        self.robot_id = "leader"
        self.position = start_pos
        self.path = []

    def set_path(self, path):
        self.path = path.copy()

    def move(self):
        if self.path:
            self.position = self.path.pop(0)

    def communicate(self, bus):
        bus.publish_position(self.robot_id, self.position)


def draw_reward_plot(rewards, filename, title):
    plt.figure()
    plt.plot(rewards)
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title(title)
    plt.grid(True)
    plt.savefig(filename)
    plt.close()


def draw_frame(ax, grid, leader, followers, goal, path, title):
    ax.clear()

    px = [p[0] for p in path]
    py = [p[1] for p in path]
    pz = [p[2] for p in path]
    ax.plot(px, py, pz, linewidth=2, label="3D A* Path")

    if grid.obstacles:
        ox = [p[0] for p in grid.obstacles]
        oy = [p[1] for p in grid.obstacles]
        oz = [p[2] for p in grid.obstacles]
        ax.scatter(ox, oy, oz, marker="s", s=80, label="Obstacles")

    ax.scatter(
        leader.position[0],
        leader.position[1],
        leader.position[2],
        s=180,
        label="Leader"
    )

    for follower in followers:
        ax.scatter(
            follower.position[0],
            follower.position[1],
            follower.position[2],
            s=130,
            label=follower.robot_id
        )

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

    ax.scatter(goal[0], goal[1], goal[2], marker="*", s=220, label="Goal")

    ax.set_title(title)
    ax.set_xlim(0, grid.width)
    ax.set_ylim(0, grid.height)
    ax.set_zlim(0, grid.depth)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend(loc="upper left")


def run_simulation(formation_name, output_gif, reward_png):
    if formation_name == "tetrahedron":
        offsets = get_tetrahedron_offsets()
    else:
        offsets = get_triangle_3d_offsets()

    trained_followers, rewards = train_3d_followers(
        formation=formation_name,
        episodes=3000
    )

    draw_reward_plot(
        rewards,
        reward_png,
        f"3D {formation_name.capitalize()} Q-learning Reward"
    )

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
        print("3D hedefe giden yol bulunamadı.")
        return

    leader = Leader3D(start)
    leader.set_path(path)

    followers = []

    for i, offset in enumerate(offsets[1:], start=1):
        start_pos = (
            start[0] + offset[0],
            start[1] + offset[1],
            start[2] + offset[2],
        )

        follower = Follower3D(
            robot_id=f"follower_{i}",
            start_pos=start_pos,
            offset=offset
        )

        follower.q = trained_followers[i - 1].q
        follower.q.epsilon = 0.0

        followers.append(follower)

    bus = CommunicationBus3D()

    leader.communicate(bus)
    for follower in followers:
        follower.communicate(bus)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    def update(frame):
        if leader.path:
            leader.move()
            leader.communicate(bus)

            for follower in followers:
                follower.move(bus)
                follower.communicate(bus)

        draw_frame(
            ax,
            grid,
            leader,
            followers,
            goal,
            path,
            f"3D {formation_name.capitalize()} Formation with Q-learning"
        )

    anim = FuncAnimation(
        fig,
        update,
        frames=len(path) + 20,
        interval=300,
        repeat=False
    )

    anim.save(output_gif, writer=PillowWriter(fps=3))
    plt.close()

    print(f"{output_gif} oluşturuldu.")
    print(f"{reward_png} oluşturuldu.")


def main():
    run_simulation(
        formation_name="triangle",
        output_gif="simulation_3d_triangle_qlearning.gif",
        reward_png="training_rewards_3d_triangle.png"
    )

    run_simulation(
        formation_name="tetrahedron",
        output_gif="simulation_3d_tetrahedron_qlearning.gif",
        reward_png="training_rewards_3d_tetrahedron.png"
    )


if __name__ == "__main__":
    main()