from environment.grid import Grid
from algorithms.astar import astar
from agents.leader import Leader
from agents.follower import Follower
from formation.triangle import get_triangle_offsets
from training import train_follower
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from communication.communication_bus import CommunicationBus


def draw_frame(ax, grid, leader, followers, goal, path):
    ax.clear()

    for x in range(grid.width):
        for y in range(grid.height):
            ax.scatter(x, y, marker="s", s=300, edgecolors="black")

    if path:
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        ax.plot(path_x, path_y, linewidth=2)

    if grid.obstacles:
        ox = [p[0] for p in grid.obstacles]
        oy = [p[1] for p in grid.obstacles]
        ax.scatter(ox, oy, marker="s", s=300)

    ax.scatter(leader.position[0], leader.position[1], s=500, label="Leader")

    for follower in followers:
        ax.scatter(follower.position[0], follower.position[1], s=500, label=follower.robot_id)

    ax.scatter(goal[0], goal[1], s=500, marker="*", label="Goal")

    ax.set_xlim(-1, grid.width)
    ax.set_ylim(-1, grid.height)
    ax.set_aspect("equal")
    ax.grid(True)
    ax.legend(loc="upper right")

def save_reward_plot(episode_rewards):
    plt.figure()
    plt.plot(episode_rewards)
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title("Q-learning Training Reward")
    plt.grid(True)
    plt.savefig("training_rewards.png")
    plt.close()

def main():
    trained_q, episode_rewards = train_follower(episodes=3000)
    save_reward_plot(episode_rewards)
    grid = Grid(20, 20)

    grid.obstacles = {
        (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8),
        (12, 10), (12, 11), (12, 12), (12, 13), (12, 14),
        (5, 13), (6, 13), (7, 13), (8, 13)
    }

    start = (3, 3)
    goal = (17, 17)

    leader = Leader(start, robot_id="leader")

    path = astar(grid, start, goal)

    if not path:
        print("Hedefe giden yol bulunamadı.")
        return

    leader.set_path(path.copy())

    offsets = get_triangle_offsets()

    followers = [
    Follower(
        (start[0] + offsets[1][0], start[1] + offsets[1][1]),
        offsets[1],
        robot_id="follower_1",
        mode="qlearning"
    ),
    Follower(
        (start[0] + offsets[2][0], start[1] + offsets[2][1]),
        offsets[2],
        robot_id="follower_2",
        mode="qlearning"
    ),
]

    for follower in followers:
        follower.q = trained_q

    communication_bus = CommunicationBus()

    leader.communicate(communication_bus)

    for follower in followers:
        follower.communicate(communication_bus)

    fig, ax = plt.subplots()

    def update(frame):
        if leader.path:
            leader.move()
            leader.communicate(communication_bus)

            for follower in followers:
                follower.move(communication_bus)
                follower.communicate(communication_bus)

        draw_frame(ax, grid, leader, followers, goal, path)

    anim = FuncAnimation(
    fig,
    update,
    frames=len(path) + 10,
    interval=300,
    repeat=False
)

    anim.save("simulation.gif", writer=PillowWriter(fps=2))

    print("GIF oluşturuldu: simulation.gif")


if __name__ == "__main__":
    main()