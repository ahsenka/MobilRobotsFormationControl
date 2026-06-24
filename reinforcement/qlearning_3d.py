import random

class QLearning3D:
    def __init__(self, epsilon=0.25):
        self.q_table = {}
        self.actions = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1),
            (0, 0, 0)
        ]
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = epsilon

    def get_q(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        qs = [self.get_q(state, action) for action in self.actions]
        max_q = max(qs)
        return self.actions[qs.index(max_q)]

    def update(self, state, action, reward, next_state):
        old_q = self.get_q(state, action)
        max_future_q = max(self.get_q(next_state, a) for a in self.actions)

        new_q = old_q + self.alpha * (
            reward + self.gamma * max_future_q - old_q
        )

        self.q_table[(state, action)] = new_q