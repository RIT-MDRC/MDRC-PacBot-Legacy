from typing import NamedTuple
import math

class Position(NamedTuple):
    x: float  # to the right
    y: float  # up

    def dist(self, pos: "Position") -> float:
        return math.hypot(self.x - pos.x, self.y - pos.y)

    def apply_change(self, other: "Position") -> "Position":
        self.x += other.x
        self.y += other.y
        return self