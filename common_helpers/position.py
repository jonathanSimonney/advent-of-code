from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    """Class for position on an 2 dimensions board."""
    x: int
    y: int

    def get_right_pos(self):
        return Position(self.x + 1, self.y)

    def get_left_pos(self):
        return Position(self.x - 1, self.y)

    def get_top_pos(self):
        return Position(self.x, self.y - 1)

    def get_bottom_pos(self):
        return Position(self.x, self.y + 1)
