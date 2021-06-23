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
    OXYGEN = 2
    UNKNOWN = 3


class AllAdjacentSpacesExploredException(Exception):
    pass


class Robot:
    min_x_pos = 0
    min_y_pos = 0
    max_x_pos = 0
    max_y_pos = 0
    x_pos = 0
    y_pos = 0
    direction = Direction.NONE
    dict_known_pos = collections.defaultdict(lambda:  Tiles.UNKNOWN)
    return_path = []
    is_backtracking = False
    targeted_x_pos = 0
    targeted_y_pos = 0

    def __init__(self):
        self.dict_known_pos[compute_key_with_coords(self.x_pos, self.y_pos)] = Tiles.FLOOR

    def get_input(self):
        # todo implement a move logic not relying on input. robot knows where he is and what spaces are around him,
        #  so he needs to either :  keep exploring RIGHT next to him, OR go to the closest unblocked space to explore
        self._print_known_space()

        try:
            self.is_backtracking = False
            if self.dict_known_pos[compute_key_with_coords(self.targeted_x_pos, self.targeted_y_pos)] != Tiles.UNKNOWN:
                self._compute_new_target_space()
            self.direction = self._compute_direction_to_move_towards(self.targeted_x_pos, self.targeted_y_pos)
        except AllAdjacentSpacesExploredException:
            self.is_backtracking = True
            self.direction = self.return_path.pop()
        return self.direction.value

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
            if not self.is_backtracking:
                self.return_path.append(get_opposite_direction(self.direction))
        elif output_value == 2:
            print(f"oxygen tank found, at pos : {post_move_x_pos}, {post_move_y_pos}")
            # 203 too low
            print(len(self.return_path))
            # raise Exception
            self.x_pos = post_move_x_pos
            self.y_pos = post_move_y_pos
            self.dict_known_pos[compute_key_with_coords(post_move_x_pos, post_move_y_pos)] = Tiles.OXYGEN
            if not self.is_backtracking:
                self.return_path.append(get_opposite_direction(self.direction))

    def _print_known_space(self):
        dict_symbols = {
            Tiles.UNKNOWN: ' ',
            Tiles.FLOOR: '.',
            Tiles.OXYGEN: 'O',
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

    def _compute_new_target_space(self):
        if self.dict_known_pos[compute_key_with_coords(self.x_pos + 1, self.y_pos)] == Tiles.UNKNOWN:
            self._set_new_target_space(self.x_pos + 1, self.y_pos)
        elif self.dict_known_pos[compute_key_with_coords(self.x_pos - 1, self.y_pos)] == Tiles.UNKNOWN:
            self._set_new_target_space(self.x_pos - 1, self.y_pos)
        elif self.dict_known_pos[compute_key_with_coords(self.x_pos, self.y_pos + 1)] == Tiles.UNKNOWN:
            self._set_new_target_space(self.x_pos, self.y_pos + 1)
        elif self.dict_known_pos[compute_key_with_coords(self.x_pos, self.y_pos - 1)] == Tiles.UNKNOWN:
            self._set_new_target_space(self.x_pos, self.y_pos - 1)
        else:
            self._print_known_space()
            raise AllAdjacentSpacesExploredException

    def _compute_direction_to_move_towards(self, x, y):
        if x == self.x_pos + 1 and y == self.y_pos:
            return Direction.EAST
        elif x == self.x_pos - 1 and y == self.y_pos:
            return Direction.WEST
        elif x == self.x_pos and y == self.y_pos + 1:
            return Direction.NORTH
        elif x == self.x_pos and y == self.y_pos - 1:
            return Direction.SOUTH
        else:
            raise Exception

    def _set_new_target_space(self, x, y):
        self.targeted_x_pos = x
        self.targeted_y_pos = y


def get_opposite_direction(direction):
    dict_opposed_directions = {
        Direction.SOUTH: Direction.NORTH,
        Direction.NORTH: Direction.SOUTH,
        Direction.WEST: Direction.EAST,
        Direction.EAST: Direction.WEST,
    }

    return dict_opposed_directions[direction]


with open("data.txt") as f:
    content = f.readlines()

# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x) for x in content[0].strip().split(",")]

intcode_computer = IntcodeComputer(content)
robot = Robot()

intcode_computer.run_intcode_program_from_start(
    get_input_instruction=robot.get_input, send_output_instruction=robot.handle_output)
