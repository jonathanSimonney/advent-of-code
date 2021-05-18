import itertools
from enum import Enum

from year_2019.intcode_computer import IntcodeComputer


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def compute_key_with_coords(x_coord, y_coord):
    return f"x{x_coord}y{y_coord}"


def get_input():
    return 1 if compute_key_with_coords(x_pos, y_pos) in set_painted_white_panels else 0


def handle_output(value):
    global is_painting
    global robot_direction
    global x_pos
    global y_pos
    global max_x
    global max_y
    global min_x
    global min_y

    if is_painting:
        is_painting = False
        current_pos_key = compute_key_with_coords(x_pos, y_pos)
        if value == 0:
            if current_pos_key in set_painted_white_panels:
                set_painted_white_panels.remove(current_pos_key)
            set_painted_black_panels.add(current_pos_key)
        else:
            if current_pos_key in set_painted_black_panels:
                set_painted_black_panels.remove(current_pos_key)
            set_painted_white_panels.add(current_pos_key)
    else:
        is_painting = True
        modifier_direction = 1 if value == 1 else -1
        robot_direction = Direction((robot_direction.value + modifier_direction) % 4)
        if robot_direction == Direction.UP:
            y_pos += 1
            if y_pos > max_y:
                max_y = y_pos
        elif robot_direction == Direction.RIGHT:
            x_pos += 1
            if x_pos > max_x:
                max_x = x_pos
        elif robot_direction == Direction.DOWN:
            y_pos -= 1
            if y_pos < min_y:
                min_y = y_pos
        elif robot_direction == Direction.LEFT:
            x_pos -= 1
            if x_pos < min_x:
                min_x = x_pos


with open("data.txt") as f:
    content = f.readlines()


# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x) for x in content[0].strip().split(",")]
print(content)

x_pos = 0
y_pos = 0
min_x = 0
min_y = 0
max_x = 0
max_y = 0

robot_direction = Direction.UP
set_painted_white_panels = {compute_key_with_coords(x_pos, y_pos)}
set_painted_black_panels = set()
is_painting = True

intcode_computer = IntcodeComputer(content)

intcode_computer.run_intcode_program_from_start(get_input_instruction=get_input, send_output_instruction=handle_output)

# 1037 too low
print(len(set_painted_white_panels) + len(set_painted_black_panels))

print(set_painted_white_panels)

str_to_print = ''
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        if compute_key_with_coords(x, y) in set_painted_white_panels:
            str_to_print += '*'
        else:
            str_to_print += ' '
    str_to_print += '\n'

print(str_to_print)
#RKURGKGK