from algorithms.qlearning import QLearning


class Follower:
    def __init__(self, start_pos, offset, robot_id, mode="baseline"):
        self.robot_id = robot_id
        self.position = start_pos
        self.offset = offset
        self.mode = mode
        self.q = QLearning()

    def communicate(self, communication_bus):
        communication_bus.publish_position(self.robot_id, self.position)

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

    def is_position_occupied(self, new_pos, communication_bus):
        other_positions = communication_bus.get_other_positions(self.robot_id).values()
        return new_pos in other_positions

    def is_too_close_to_other_robot(self, new_pos, communication_bus):
        other_positions = communication_bus.get_other_positions(self.robot_id).values()

        for pos in other_positions:
            distance = abs(new_pos[0] - pos[0]) + abs(new_pos[1] - pos[1])

            if distance == 0:
                return True

        return False

    def calculate_reward(self, old_distance, new_distance, collision_risk=False):
        if collision_risk:
            return -30

        if new_distance == 0:
            return 20

        if new_distance < old_distance:
            return 5

        if new_distance == old_distance:
            return -1

        return -5

    def move_baseline(self, communication_bus):
        leader_pos = communication_bus.get_position("leader")

        if leader_pos is None:
            return

        target = self.get_target_position(leader_pos)

        x, y = self.position
        tx, ty = target

        dx = tx - x
        dy = ty - y

        candidate_positions = []

        if dx != 0:
            candidate_positions.append((x + (1 if dx > 0 else -1), y))

        if dy != 0:
            candidate_positions.append((x, y + (1 if dy > 0 else -1)))

        candidate_positions.append(self.position)

        best_position = self.position
        best_distance = self.calculate_distance(leader_pos)

        for candidate in candidate_positions:
            if self.is_too_close_to_other_robot(candidate, communication_bus):
                continue

            candidate_distance = abs(candidate[0] - target[0]) + abs(candidate[1] - target[1])

            if candidate_distance < best_distance:
                best_distance = candidate_distance
                best_position = candidate

        self.position = best_position

    def move_qlearning(self, communication_bus):
        leader_pos = communication_bus.get_position("leader")

        if leader_pos is None:
            return

        state = self.get_state(leader_pos)
        old_distance = self.calculate_distance(leader_pos)

        action = self.q.choose_action(state)

        new_pos = (
            self.position[0] + action[0],
            self.position[1] + action[1]
        )

        collision_risk = self.is_too_close_to_other_robot(new_pos, communication_bus)

        if not collision_risk:
            self.position = new_pos

        next_state = self.get_state(leader_pos)
        new_distance = self.calculate_distance(leader_pos)

        reward = self.calculate_reward(old_distance, new_distance, collision_risk)

        self.q.update(state, action, reward, next_state)

    def move(self, communication_bus):
        if self.mode == "qlearning":
            self.move_qlearning(communication_bus)
        else:
            self.move_baseline(communication_bus)