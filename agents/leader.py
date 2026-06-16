class Leader:
    def __init__(self, start_pos, robot_id="leader"):
        self.robot_id = robot_id
        self.position = start_pos
        self.path = []

    def set_path(self, path):
        self.path = path

    def move(self):
        if self.path:
            self.position = self.path.pop(0)

    def communicate(self, communication_bus):
        communication_bus.publish_position(self.robot_id, self.position)