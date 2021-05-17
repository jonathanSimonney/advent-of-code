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
        elif robot_direction == Direction.RIGHT:
            x_pos += 1
        elif robot_direction == Direction.DOWN:
            y_pos -= 1
        elif robot_direction == Direction.LEFT:
            x_pos -= 1


with open("data.txt") as f:
    content = f.readlines()


# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x) for x in content[0].strip().split(",")]
print(content)

x_pos = 0
y_pos = 0
robot_direction = Direction.UP
set_painted_white_panels = set(compute_key_with_coords(x_pos, y_pos))
set_painted_black_panels = set()
is_painting = True

intcode_computer = IntcodeComputer(content)

intcode_computer.run_intcode_program_from_start(get_input_instruction=get_input, send_output_instruction=handle_output)

# 1037 too low
print(len(set_painted_white_panels) + len(set_painted_black_panels))

print(set_painted_white_panels)
# TODO find lowes x and y in the set, and append this x and this y before drawing ascii art style the pic of the code
# identification needed.
