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


def compute_x_impact_coords(current_ball_pos, previous_ball_pos, dict_tiles_current, pos_paddle):
    global max_x
    global max_y

    is_ball_moving_down = current_ball_pos['y'] > previous_ball_pos['y']
    is_ball_moving_right = current_ball_pos['x'] > previous_ball_pos['x']
    multiplicator_coeff = 1 if is_ball_moving_right else -1

    print(is_ball_moving_down, is_ball_moving_right)

    if is_ball_moving_down:
        nb_moves_left = pos_paddle['y'] - current_ball_pos['y']
        return current_ball_pos['x'] + nb_moves_left * multiplicator_coeff
    else:
        return current_ball_pos['x']


def get_input():
    global dict_tiles
    global max_x
    global max_y
    global paddle_pos
    global ball_pos
    global ball_pos_n1
    global current_impact_point_x


    if ball_pos_n1 == {}:
        paint_tiles(dict_tiles, max_x, max_y)
        return 0

    print(ball_pos)
    print(ball_pos_n1)
    print(paddle_pos)

    expected_impact_ball_x = compute_x_impact_coords(ball_pos, ball_pos_n1, dict_tiles, paddle_pos)
    current_impact_point_x = expected_impact_ball_x
    print(expected_impact_ball_x, paddle_pos)
    paint_tiles(dict_tiles, max_x, max_y)

    if expected_impact_ball_x == paddle_pos['x']:
        print('ball going ALREADY on paddle')
        if paddle_pos['y'] == ball_pos['y'] + 1 and ball_pos['y'] > ball_pos_n1['y']:
            return -1 if ball_pos['x'] > ball_pos_n1['x'] else 1
        # return int(input("override 0 ?"))
        return 0
    elif expected_impact_ball_x > paddle_pos['x']:
        print('ball going on right of paddle, let\'s go right')
        # return int(input("override 1 ?"))
        return 1
    else:
        print('ball going on left of paddle, let\'s go left')
        # return int(input("override -1 ?"))
        return -1


def handle_output(value):
    global dict_tiles
    global painted_tile
    global max_x
    global max_y
    global paddle_pos
    global ball_pos
    global ball_pos_n1

    if 'x' not in painted_tile:
        painted_tile['x'] = value
        return

    if 'y' not in painted_tile:
        painted_tile['y'] = value
        return

    if 'tile_type' not in painted_tile:
        if painted_tile['x'] == -1 and painted_tile['y'] == 0:
            painted_tile['tile_type'] = value
        else:
            painted_tile['tile_type'] = DrawnObjects(value)
        dict_tiles[compute_key_with_coords(painted_tile)] = painted_tile['tile_type']

        if painted_tile['x'] > max_x:
            max_x = painted_tile['x']

        if painted_tile['y'] > max_y:
            max_y = painted_tile['y']

        if painted_tile['tile_type'] == DrawnObjects.BALL:
            ball_pos_n1 = ball_pos
            ball_pos = painted_tile
        elif painted_tile['tile_type'] == DrawnObjects.PADDLE:
            paddle_pos = painted_tile
        painted_tile = {}
        return


def paint_tiles(dict_tiles_to_paint, max_x_to_paint, max_y_to_paint):
    global current_impact_point_x
    global paddle_pos

    dict_symbols = {
        DrawnObjects.EMPTY: ' ',
        DrawnObjects.WALL: '.',
        DrawnObjects.BLOCK: 'X',
        DrawnObjects.PADDLE: '_',
        DrawnObjects.BALL: 'O',
    }

    str_to_print = ''
    for y in range(max_y_to_paint + 1):
        for x in range(max_x_to_paint + 1):
            if y == paddle_pos['y'] and x == current_impact_point_x:
                str_to_print += 'I'
            else:
                str_to_print += dict_symbols[dict_tiles_to_paint[compute_key_with_coords({'x': x, 'y': y})]]
        str_to_print += '\n'

    print(str_to_print)
    print(f"score: {dict_tiles_to_paint[compute_key_with_coords({'x': -1, 'y': 0})]}")


with open("data.txt") as f:
    content = f.readlines()


# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x) for x in content[0].strip().split(",")]

painted_tile = {}
dict_tiles = {}
ball_pos_n1 = {}
ball_pos = {}
paddle_pos = {}
max_x = 0
max_y = 0
current_impact_point_x = -1

intcode_computer = IntcodeComputer(content)

intcode_computer.run_intcode_program_from_start(get_input_instruction=get_input, send_output_instruction=handle_output)

paint_tiles(dict_tiles, max_x, max_y)
