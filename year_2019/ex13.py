from enum import Enum

from year_2019.intcode_computer import IntcodeComputer


class DrawnObjects(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


def compute_key_with_coords(tile_dict):
    return f"x{tile_dict['x']}y{tile_dict['y']}"


def get_input():
    raise Exception("no input logic specified")


def handle_output(value):
    global dict_tiles
    global painted_tile
    global max_x
    global max_y

    if 'x' not in painted_tile:
        painted_tile['x'] = value
        return

    if 'y' not in painted_tile:
        painted_tile['y'] = value
        return

    if 'tile_type' not in painted_tile:
        painted_tile['tile_type'] = DrawnObjects(value)
        dict_tiles[compute_key_with_coords(painted_tile)] = painted_tile['tile_type']

        if painted_tile['x'] > max_x:
            max_x = painted_tile['x']

        if painted_tile['y'] > max_y:
            max_y = painted_tile['y']
        painted_tile = {}
        return


with open("data.txt") as f:
    content = f.readlines()


# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x) for x in content[0].strip().split(",")]

painted_tile = {}
dict_tiles = {}
max_x = 0
max_y = 0


intcode_computer = IntcodeComputer(content)

intcode_computer.run_intcode_program_from_start(get_input_instruction=get_input, send_output_instruction=handle_output)
print(dict_tiles)

dict_symbols = {
    DrawnObjects.EMPTY: ' ',
    DrawnObjects.WALL: '.',
    DrawnObjects.BLOCK: 'X',
    DrawnObjects.PADDLE: '_',
    DrawnObjects.BALL: 'O',
}

str_to_print = ''
for y in range(max_y + 1):
    for x in range(max_x + 1):
        str_to_print += dict_symbols[dict_tiles[compute_key_with_coords({'x': x, 'y': y})]]
    str_to_print += '\n'

print(str_to_print)
print(str_to_print.count('X'))
