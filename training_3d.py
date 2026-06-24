from agents.follower_3d import Follower3D
from communication.communication_bus_3d import CommunicationBus3D
from formation.formations3d import get_triangle_3d_offsets, get_tetrahedron_offsets


def train_3d_followers(formation="triangle", episodes=3000):
    leader_pos = (10, 10, 8)

    if formation == "tetrahedron":
        offsets = get_tetrahedron_offsets()
    else:
        offsets = get_triangle_3d_offsets()

    followers = []

    for i, offset in enumerate(offsets[1:], start=1):
        followers.append(
            Follower3D(
                robot_id=f"follower_{i}",
                start_pos=(0, 0, 0),
                offset=offset
            )
        )

    episode_rewards = []

    for ep in range(episodes):
        bus = CommunicationBus3D()
        bus.publish_position("leader", leader_pos)

        for follower in followers:
            follower.position = (0, 0, 0)
            follower.communicate(bus)

        total_reward = 0

        for step in range(120):
            for follower in followers:
                reward = follower.move(bus)
                follower.communicate(bus)
                total_reward += reward

        episode_rewards.append(total_reward)

        if ep % 100 == 0:
            print(f"3D {formation} Episode {ep} | Reward: {total_reward}")

    for follower in followers:
        follower.q.epsilon = 0.0

    return followers, episode_rewards