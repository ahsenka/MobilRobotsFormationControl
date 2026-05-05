# agents/follower.py

class Follower:
    def __init__(self, start_pos, offset):
        self.position = start_pos
        self.offset = offset

    def move(self, leader_pos):
        target = (
            leader_pos[0] + self.offset[0],
            leader_pos[1] + self.offset[1]
        )

        x, y = self.position
        tx, ty = target

        dx = tx - x
        dy = ty - y

        if abs(dx) > abs(dy):
            x += 1 if dx > 0 else -1
        elif dy != 0:
            y += 1 if dy > 0 else -1

        self.position = (x, y)

