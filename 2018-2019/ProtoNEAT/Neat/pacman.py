from neat import DefaultGenome


class PacMan(DefaultGenome):
    def __init__(self, key):
        super().__init__(key)
        self.points_earned = []

    def get_points(self, points):
        self.points_earned.append(points)
