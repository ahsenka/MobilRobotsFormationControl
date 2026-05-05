class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = set()

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def is_obstacle(self, pos):
        return pos in self.obstacles

    def neighbors(self, pos):
        x, y = pos
        candidates = [
            (x+1, y),
            (x-1, y),
            (x, y+1),
            (x, y-1)
        ]
        return [p for p in candidates if self.in_bounds(p) and not self.is_obstacle(p)]