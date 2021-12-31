from dataclasses import dataclass
from typing import Union


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


@dataclass(frozen=True)
class ThreeDPosition:
    """Class for position on an 3 dimensions board."""
    x: int
    y: int
    z: int

    def get_point_rotated_over_x_axis(self):
        return ThreeDPosition(self.x, -self.z, self.y)

    def get_point_rotated_over_y_axis(self):
        return ThreeDPosition(self.z, self.y, -self.x)

    def get_point_rotated_over_z_axis(self):
        return ThreeDPosition(self.y, -self.x, self.z)


def get_position_relative_to_another(pos_reference: ThreeDPosition, other_pos: ThreeDPosition) -> ThreeDPosition:
    res_pos_x = other_pos.x - pos_reference.x
    res_pos_y = other_pos.y - pos_reference.y
    res_pos_z = other_pos.z - pos_reference.z

    return ThreeDPosition(res_pos_x, res_pos_y, res_pos_z)


def compute_manhattan_dist(pos_1: ThreeDPosition, pos_2: ThreeDPosition) -> int:
    diff_pos_x = pos_2.x - pos_1.x
    diff_pos_y = pos_2.y - pos_1.y
    diff_pos_z = pos_2.z - pos_1.z

    return abs(diff_pos_x) + abs(diff_pos_y) + abs(diff_pos_z)


@dataclass(frozen=True)
class Cuboid:
    """Class for a cube shape on an 3 dimensions board."""
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    def compute_volume(self) -> int:
        return (self.z_max + 1 - self.z_min) * (self.y_max + 1 - self.y_min) * (self.x_max + 1 - self.x_min)


def compute_intersection_cuboid(cuboid_1: Cuboid, cuboid_2: Cuboid) -> Union[Cuboid, None]:
    would_be_x_min = max(cuboid_1.x_min, cuboid_2.x_min)
    would_be_x_max = min(cuboid_1.x_max, cuboid_2.x_max)
    would_be_y_min = max(cuboid_1.y_min, cuboid_2.y_min)
    would_be_y_max = min(cuboid_1.y_max, cuboid_2.y_max)
    would_be_z_min = max(cuboid_1.z_min, cuboid_2.z_min)
    would_be_z_max = min(cuboid_1.z_max, cuboid_2.z_max)

    if would_be_x_min <= would_be_x_max and would_be_y_min <= would_be_y_max and would_be_z_min <= would_be_z_max:
        return Cuboid(
            would_be_x_min,
            would_be_x_max,
            would_be_y_min,
            would_be_y_max,
            would_be_z_min,
            would_be_z_max
        )
