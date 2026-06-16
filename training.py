from agents.follower import Follower
from formation.triangle import get_triangle_offsets
from communication.communication_bus import CommunicationBus


def train_follower(episodes=1000):
    leader_pos = (5, 5)
    offsets = get_triangle_offsets()

    follower = Follower((0, 0), offsets[1], robot_id="training_follower", mode="qlearning")

    for ep in range(episodes):
        communication_bus = CommunicationBus()

        follower.position = (0, 0)

        communication_bus.publish_position("leader", leader_pos)
        follower.communicate(communication_bus)

        for step in range(100):
            follower.move(communication_bus)
            follower.communicate(communication_bus)

        if ep % 100 == 0:
            print(f"Episode {ep} tamamlandı")

    return follower.q