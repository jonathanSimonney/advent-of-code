import collections
from enum import Enum

from year_2019.intcode_computer import IntcodeComputer


def compute_key_with_coords(pos_x, pos_y):
    return f"x{pos_x}y{pos_y}"


class Direction(Enum):
    NONE = 0
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class Tiles(Enum):
    WALL = 0
    FLOOR = 1
    UNKNOWN = 2


class Robot:
    min_x_pos = 0
    min_y_pos = 0
    max_x_pos = 0
    max_y_pos = 0
    x_pos = 0
    y_pos = 0
    direction = Direction.NONE
    dict_known_pos = collections.defaultdict(lambda:  Tiles.UNKNOWN)

    def __init__(self):
        self.dict_known_pos[compute_key_with_coords(self.x_pos, self.y_pos)] = Tiles.FLOOR

    def get_input(self):
        # todo implement a move logic not relying on input. robot knows where he is and what spaces are around him,
        #  so he needs to either :  keep exploring RIGHT next to him, OR go to the closest unblocked space to explore
        self._print_known_space()
        input_number = int(input('please write direction'))
        self.direction = Direction(input_number)
        return input_number

    def handle_output(self, output_value):
        post_move_x_pos = self.x_pos
        post_move_y_pos = self.y_pos
        if self.direction == Direction.SOUTH:
            post_move_y_pos -= 1
            if post_move_y_pos < self.min_y_pos:
                self.min_y_pos = post_move_y_pos
        elif self.direction == Direction.NORTH:
            post_move_y_pos += 1
            if post_move_y_pos > self.max_y_pos:
                self.max_y_pos = post_move_y_pos
        elif self.direction == Direction.WEST:
            post_move_x_pos -= 1
            if post_move_x_pos < self.min_x_pos:
                self.min_x_pos = post_move_x_pos
        elif self.direction == Direction.EAST:
            post_move_x_pos += 1
            if post_move_x_pos > self.max_x_pos:
                self.max_x_pos = post_move_x_pos

        if output_value == 0:
            self.dict_known_pos[compute_key_with_coords(post_move_x_pos, post_move_y_pos)] = Tiles.WALL
        elif output_value == 1:
            self.x_pos = post_move_x_pos
            self.y_pos = post_move_y_pos
            self.dict_known_pos[compute_key_with_coords(post_move_x_pos, post_move_y_pos)] = Tiles.FLOOR
        elif output_value == 2:
            print(f"oxygen tank found, at pos : {post_move_x_pos}, {post_move_y_pos}")
            self.x_pos = post_move_x_pos
            self.y_pos = post_move_y_pos

    def _print_known_space(self):
        dict_symbols = {
            Tiles.UNKNOWN: ' ',
            Tiles.FLOOR: '.',
            Tiles.WALL: '#',
        }

        str_to_print = ''
        for y in range(self.min_y_pos, self.max_y_pos + 1):
            for x in range(self.min_x_pos, self.max_x_pos + 1):
                if y == self.y_pos and x == self.x_pos:
                    str_to_print += 'D'
                else:
                    str_to_print += dict_symbols[self.dict_known_pos[compute_key_with_coords(x, y)]]
            str_to_print += '\n'

        print(str_to_print)

with open("data.txt") as f:
    content = f.readlines()

# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x) for x in content[0].strip().split(",")]

intcode_computer = IntcodeComputer(content)
robot = Robot()

intcode_computer.run_intcode_program_from_start(
    get_input_instruction=robot.get_input, send_output_instruction=robot.handle_output)
