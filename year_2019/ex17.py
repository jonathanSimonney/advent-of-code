import collections
from enum import Enum
from typing import TypedDict

from year_2019.intcode_computer import IntcodeComputer
from dataclasses import dataclass


class Direction(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4


class TypesPosition(Enum):
    SCAFFOLD = 0
    SPACE = 1
    VACUUM_ROBOT = 2


class RobotMove(TypedDict):
    direction: Direction
    nb_move: int
    turned_left: bool


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


class AsciiReader:
    _buffer_str = ""

    def __init__(self):
        pass

    def get_input(self):
        pass

    def handle_output(self, output_str: str):
        self._buffer_str += chr(int(output_str))

    def get_result_str(self):
        return self._buffer_str


def get_vacuum_robot_dir(robot_pos: Position, set_scaffold_pos: set[Position], current_dir: Direction = None)\
        -> Direction:
    if robot_pos.get_top_pos() in set_scaffold_pos:
        if current_dir != Direction.BOTTOM and current_dir != Direction.TOP:
            return Direction.TOP
    if robot_pos.get_bottom_pos() in set_scaffold_pos:
        if current_dir != Direction.TOP and current_dir != Direction.BOTTOM:
            return Direction.BOTTOM
    if robot_pos.get_left_pos() in set_scaffold_pos:
        if current_dir != Direction.LEFT and current_dir != Direction.RIGHT:
            return Direction.LEFT
    if robot_pos.get_right_pos() in set_scaffold_pos:
        if current_dir != Direction.LEFT and current_dir != Direction.RIGHT:
            return Direction.RIGHT

    raise RuntimeError("no direction found matching the constraints")


def get_simple_robot_path(scaffold_pos_set: set[Position], robot_pos: Position) -> list[RobotMove]:
    virtually_walked_scaffold: set[Position] = set()
    list_moves: list[RobotMove] = []

    def walk_robot_in_dir(from_pos: Position, direction: Direction) -> Position:
        current_move = {'direction': direction, 'nb_move': 0}

        next_pos = from_pos.get_pos_in_direction(direction)
        while next_pos in scaffold_pos_set:
            current_move['nb_move'] += 1
            virtually_walked_scaffold.add(next_pos)
            from_pos = next_pos
            next_pos = from_pos.get_pos_in_direction(direction)

        if len(list_moves) == 0:
            current_move['turned_left'] = True
        else:
            prev_move = list_moves[-1]
            current_move['turned_left'] = \
                True if (prev_move['direction'].value - current_move['direction'].value) % 4 == 1 else False
        list_moves.append(current_move)
        return from_pos

    vacuum_robot_direction = None
    while len(scaffold_pos_set) != len(virtually_walked_scaffold):
        vacuum_robot_direction = get_vacuum_robot_dir(robot_pos, scaffold_pos_set, vacuum_robot_direction)
        robot_pos = walk_robot_in_dir(robot_pos, vacuum_robot_direction)

    return list_moves


with open("data.txt") as f:
    content = f.readlines()

# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x) for x in content[0].strip().split(",")]

intcode_computer = IntcodeComputer(content)
ascii_reader = AsciiReader()

intcode_computer.run_intcode_program_from_start(
    get_input_instruction=ascii_reader.get_input, send_output_instruction=ascii_reader.handle_output)

print(ascii_reader.get_result_str())
shuttle_space_array: list[str] = ascii_reader.get_result_str().split('\n')

dict_symbols = {
     '#': TypesPosition.SCAFFOLD,
     '.': TypesPosition.SPACE,
     '^': TypesPosition.VACUUM_ROBOT,
}

scaffold_pos_set = set()
vacuum_robot_init_pos = None

for y, line_shuttle in enumerate(shuttle_space_array):
    for x, shuttle_char in enumerate(line_shuttle):
        if dict_symbols[shuttle_char] == TypesPosition.SCAFFOLD:
            scaffold_pos_set.add(Position(x, y))
        elif dict_symbols[shuttle_char] == TypesPosition.VACUUM_ROBOT:
            vacuum_robot_init_pos = Position(x, y)

robot_moves = get_simple_robot_path(scaffold_pos_set, vacuum_robot_init_pos)
print(','.join([f"{'L' if move['turned_left'] else 'R'},{move['nb_move']}" for move in robot_moves]))
