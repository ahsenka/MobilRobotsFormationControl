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

        # basit yaklaşma (greedy)
        if x < tx:
            x += 1
        elif x > tx:
            x -= 1

        if y < ty:
            y += 1
        elif y > ty:
            y -= 1

        self.position = (x, y)