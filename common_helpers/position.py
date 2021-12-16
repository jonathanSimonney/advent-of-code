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

    def get_top_right_pos(self):
        return Position(self.x + 1, self.y - 1)

    def get_top_left_pos(self):
        return Position(self.x - 1, self.y - 1)

    def get_bottom_left_pos(self):
        return Position(self.x - 1, self.y + 1)

    def get_bottom_right_pos(self):
        return Position(self.x + 1, self.y + 1)

    def get_all_adjacent_pos(self):
        return [
            self.get_bottom_right_pos(),
            self.get_bottom_pos(),
            self.get_bottom_left_pos(),
            self.get_left_pos(),
            self.get_top_left_pos(),
            self.get_top_pos(),
            self.get_top_right_pos(),
            self.get_right_pos()
        ]

    def get_all_adjacent_pos_without_diagonal(self):
        return [
            self.get_bottom_pos(),
            self.get_left_pos(),
            self.get_top_pos(),
            self.get_right_pos()
        ]


def print_ascii_with_set_position(position_set: set[Position]):
    min_x = 0
    min_y = 0
    max_x = None
    max_y = None

    for pos in position_set:
        if max_x is None:
            max_x = pos.x
            max_y = pos.y
        else:
            if pos.x < min_x:
                min_x = pos.x
            if pos.x > max_x:
                max_x = pos.x
            if pos.y < min_y:
                min_y = pos.y
            if pos.y > max_y:
                max_y = pos.y

    str_to_print = ''
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if Position(x, y) in position_set:
                str_to_print += '*'
            else:
                str_to_print += ' '
        str_to_print += '\n'

    print(str_to_print)
