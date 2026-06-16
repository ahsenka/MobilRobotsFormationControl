from agents.follower import Follower
from formation.triangle import get_triangle_offsets
from communication.communication_bus import CommunicationBus


def train_follower(episodes=3000):
    leader_pos = (10, 10)
    offsets = get_triangle_offsets()

    follower = Follower(
        (0, 0),
        offsets[1],
        robot_id="training_follower",
        mode="qlearning"
    )

    episode_rewards = []

    for ep in range(episodes):
        communication_bus = CommunicationBus()
        follower.position = (0, 0)

        communication_bus.publish_position("leader", leader_pos)
        follower.communicate(communication_bus)

        total_reward = 0

        for step in range(100):
            old_distance = follower.calculate_distance(leader_pos)

            follower.move(communication_bus)
            follower.communicate(communication_bus)

            new_distance = follower.calculate_distance(leader_pos)

            reward = follower.calculate_reward(old_distance, new_distance)
            total_reward += reward

        episode_rewards.append(total_reward)

        if ep % 100 == 0:
            print(f"Episode {ep} tamamlandı | Total Reward: {total_reward}")

    follower.q.epsilon = 0.0

    return follower.q, episode_rewards