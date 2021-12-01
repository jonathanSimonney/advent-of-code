import copy
from enum import Enum
from typing import TypedDict, Callable

from year_2019.intcode_computer import IntcodeComputer
from dataclasses import dataclass


class Direction(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4


class TypesPosition(Enum):
    WALL = 0
    SPACE = 1


@dataclass(frozen=True)
class Position:
    """Class for position on an 2 dimensions board."""
    x: int
    y: int

    def get_pos_in_direction(self, direction: Direction):
        if direction == Direction.TOP:
            return self.get_top_pos()
        elif direction == Direction.BOTTOM:
            return self.get_bottom_pos()
        elif direction == Direction.RIGHT:
            return self.get_right_pos()
        elif direction == Direction.LEFT:
            return self.get_left_pos()

    def get_right_pos(self):
        return Position(self.x + 1, self.y)

    def get_left_pos(self):
        return Position(self.x - 1, self.y)

    def get_top_pos(self):
        return Position(self.x, self.y - 1)

    def get_bottom_pos(self):
        return Position(self.x, self.y + 1)


# objective data struct :
# {'@': ['a': 12, 'B': 23, ..., 'X': 11],
#  'a': ['B': 23, ..., 'X': 11],
#  ...,
#  'X': ['a': 12, 'B': 23, ..., 'x': 11]
# }
def parse_content(current_maze: list[str]):
    list_empty = []
    first_pos: Position
    for y, line in enumerate(current_maze):
        for x, char in enumerate(line):
            if char == '@':
                first_pos = Position(x, y)
            elif char == '#':
                dict_pos


with open("data.txt") as f:
    content = f.readlines()

parse_content(content)

# you may also want to remove whitespace characters like `\n` at the end of each line


