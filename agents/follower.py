from algorithms.qlearning import QLearning


class Follower:
    def __init__(self, start_pos, offset, mode="baseline"):
        self.position = start_pos
        self.offset = offset
        self.mode = mode
        self.q = QLearning()

    def get_target_position(self, leader_pos):
        return (
            leader_pos[0] + self.offset[0],
            leader_pos[1] + self.offset[1]
        )

    def get_state(self, leader_pos):
        target = self.get_target_position(leader_pos)

        return (
            target[0] - self.position[0],
            target[1] - self.position[1]
        )

    def calculate_distance(self, leader_pos):
        target = self.get_target_position(leader_pos)

        return abs(self.position[0] - target[0]) + abs(self.position[1] - target[1])

    def calculate_reward(self, old_distance, new_distance):
        if new_distance == 0:
            return 20

        if new_distance < old_distance:
            return 5

        if new_distance == old_distance:
            return -1

        return -5

    def move_baseline(self, leader_pos):
        target = self.get_target_position(leader_pos)

        x, y = self.position
        tx, ty = target

        dx = tx - x
        dy = ty - y

        if abs(dx) > abs(dy):
            x += 1 if dx > 0 else -1
        elif dy != 0:
            y += 1 if dy > 0 else -1

        self.position = (x, y)

    def move_qlearning(self, leader_pos):
        state = self.get_state(leader_pos)
        old_distance = self.calculate_distance(leader_pos)

        action = self.q.choose_action(state)

        new_pos = (
            self.position[0] + action[0],
            self.position[1] + action[1]
        )

        self.position = new_pos

        next_state = self.get_state(leader_pos)
        new_distance = self.calculate_distance(leader_pos)

        reward = self.calculate_reward(old_distance, new_distance)

        self.q.update(state, action, reward, next_state)

    def move(self, leader_pos):
        if self.mode == "qlearning":
            self.move_qlearning(leader_pos)
        else:
            self.move_baseline(leader_pos)