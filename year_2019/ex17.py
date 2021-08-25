from enum import Enum

from year_2019.intcode_computer import IntcodeComputer
from dataclasses import dataclass


class Direction(Enum):
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4


class TypesPosition(Enum):
    SCAFFOLD = 0
    SPACE = 1
    VACUUM_ROBOT = 2


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


def get_all_intersections_on_scaffold(scaffold_pos_set: set[Position], robot_pos: Position) -> list[Position]:
    virtually_walked_scaffold: set[Position] = set()
    list_intersections: list[Position] = []

    def walk_robot_in_dir(from_pos: Position, direction: Direction) -> Position:
        next_pos = from_pos.get_pos_in_direction(direction)
        while next_pos in scaffold_pos_set:
            if next_pos in virtually_walked_scaffold:
                list_intersections.append(next_pos)
            virtually_walked_scaffold.add(next_pos)
            from_pos = next_pos
            next_pos = from_pos.get_pos_in_direction(direction)

        return from_pos

    vacuum_robot_direction = None
    while len(scaffold_pos_set) != len(virtually_walked_scaffold):
        vacuum_robot_direction = get_vacuum_robot_dir(robot_pos, scaffold_pos_set, vacuum_robot_direction)
        robot_pos = walk_robot_in_dir(robot_pos, vacuum_robot_direction)

    return list_intersections


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

list_intersections = get_all_intersections_on_scaffold(scaffold_pos_set, vacuum_robot_init_pos)

acc = 0
for intersection in list_intersections:
    acc += intersection.x * intersection.y

print(acc)
