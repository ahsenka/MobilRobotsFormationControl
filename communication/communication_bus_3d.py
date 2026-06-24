class CommunicationBus3D:
    def __init__(self):
        self.robot_states = {}

    def publish_position(self, robot_id, position):
        self.robot_states[robot_id] = position

    def get_position(self, robot_id):
        return self.robot_states.get(robot_id)

    def get_other_positions(self, robot_id):
        return {
            rid: pos
            for rid, pos in self.robot_states.items()
            if rid != robot_id
        }

    def get_all_positions(self):
        return self.robot_states.copy()