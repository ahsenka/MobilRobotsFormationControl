from reinforcement.qlearning_3d import QLearning3D


class Follower3D:
    def __init__(self, robot_id, start_pos, offset):
        self.robot_id = robot_id
        self.position = start_pos
        self.offset = offset
        self.q = QLearning3D()

    def communicate(self, bus):
        bus.publish_position(self.robot_id, self.position)

    def get_target_position(self, leader_pos):
        return (
            leader_pos[0] + self.offset[0],
            leader_pos[1] + self.offset[1],
            leader_pos[2] + self.offset[2],
        )

    def get_state(self, leader_pos):
        target = self.get_target_position(leader_pos)
        return (
            target[0] - self.position[0],
            target[1] - self.position[1],
            target[2] - self.position[2],
        )

    def distance_to_target(self, leader_pos):
        target = self.get_target_position(leader_pos)
        return (
            abs(target[0] - self.position[0]) +
            abs(target[1] - self.position[1]) +
            abs(target[2] - self.position[2])
        )

    def is_collision_risk(self, new_pos, bus):
        for rid, pos in bus.get_other_positions(self.robot_id).items():
            if new_pos == pos:
                return True
        return False

    def calculate_reward(self, old_distance, new_distance, collision_risk):
        if collision_risk:
            return -30

        if new_distance == 0:
            return 25

        if new_distance < old_distance:
            return 8

        if new_distance == old_distance:
            return -1

        return -8

    def move(self, bus):
        leader_pos = bus.get_position("leader")
        if leader_pos is None:
            return 0

        state = self.get_state(leader_pos)
        old_distance = self.distance_to_target(leader_pos)

        action = self.q.choose_action(state)

        new_pos = (
            self.position[0] + action[0],
            self.position[1] + action[1],
            self.position[2] + action[2],
        )

        collision_risk = self.is_collision_risk(new_pos, bus)

        if not collision_risk:
            self.position = new_pos

        next_state = self.get_state(leader_pos)
        new_distance = self.distance_to_target(leader_pos)

        reward = self.calculate_reward(
            old_distance,
            new_distance,
            collision_risk
        )

        self.q.update(state, action, reward, next_state)

        return reward