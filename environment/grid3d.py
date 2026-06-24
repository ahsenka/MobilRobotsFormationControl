class Grid3D:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.obstacles = set()

    def in_bounds(self, pos):
        x, y, z = pos
        return (
            0 <= x < self.width and
            0 <= y < self.height and
            0 <= z < self.depth
        )

    def is_obstacle(self, pos):
        return pos in self.obstacles

    def neighbors(self, pos):
        x, y, z = pos

        candidates = [
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1),
        ]

        return [
            p for p in candidates
            if self.in_bounds(p) and not self.is_obstacle(p)
        ]