import collections


# s and n are all "complete" move, e and w are also complete move, BUT se and nw move move only HALF in east or in west
def compute_str_coords_tile(str_path_to_tile):
    was_previous_move_on_y_axis = False
    x_coord = 0
    y_coord = 0
    for char in str_path_to_tile:
        if char == 'n':
            y_coord += 1
            was_previous_move_on_y_axis = True
        elif char == 's':
            y_coord -= 1
            was_previous_move_on_y_axis = True
        elif char == 'e':
            if was_previous_move_on_y_axis:
                x_coord += 0.5
                was_previous_move_on_y_axis = False
            else:
                x_coord += 1
        elif char == 'w':
            if was_previous_move_on_y_axis:
                x_coord -= 0.5
                was_previous_move_on_y_axis = False
            else:
                x_coord -= 1
        else:
            raise ValueError("invalid char in str, ", char)

    return f"{x_coord} {y_coord}"


with open("data.txt") as f:
    content = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line

dict_flipped_tiles = collections.defaultdict(lambda: False)

for path_to_tile in content:
    dict_flipped_tiles[compute_str_coords_tile(path_to_tile)] = not dict_flipped_tiles[compute_str_coords_tile(path_to_tile)]

print(sum(1 for value in dict_flipped_tiles.values() if value))
