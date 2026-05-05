from agents.follower import Follower
from formation.triangle import get_triangle_offsets


def train_follower(episodes=1000):
    leader_pos = (5, 5)
    offsets = get_triangle_offsets()

    follower = Follower((0, 0), offsets[1], mode="qlearning")

    for ep in range(episodes):
        follower.position = (0, 0)

        for step in range(100):
            follower.move(leader_pos)

        if ep % 100 == 0:
            print(f"Episode {ep} tamamlandı")

    return follower.q