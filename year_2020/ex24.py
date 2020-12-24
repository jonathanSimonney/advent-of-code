import collections


def compute_list_neighbours_coordinates(tile_coordinates):
    coordinates_array = tile_coordinates.split(" ")
    x_pos = float(coordinates_array[0])
    y_pos = float(coordinates_array[1])

    east_neighbour_coords = f"{x_pos + 1} {y_pos}"
    west_neighbour_coords = f"{x_pos - 1} {y_pos}"
    north_west_neighbour_coords = f"{x_pos - 0.5} {y_pos + 1}"
    south_west_neighbour_coords = f"{x_pos - 0.5} {y_pos - 1}"
    north_east_neighbour_coords = f"{x_pos + 0.5} {y_pos + 1}"
    south_east_neighbour_coords = f"{x_pos + 0.5} {y_pos - 1}"

    return [east_neighbour_coords, west_neighbour_coords, north_west_neighbour_coords, south_west_neighbour_coords, north_east_neighbour_coords, south_east_neighbour_coords]


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

    return f"{float(x_coord)} {float(y_coord)}"


def does_this_tile_need_to_flip(dict_tiles, tile_coord):
    list_neighbour_coordinates = compute_list_neighbours_coordinates(tile_coord)
    nb_black_neighbour = sum(1 for coord_neighbour in list_neighbour_coordinates if
                             coord_neighbour in dict_tiles and dict_tiles[coord_neighbour])

    is_tile_black = tile_coord in dict_tiles and dict_tiles[tile_coord]

    if is_tile_black and (nb_black_neighbour == 0 or nb_black_neighbour > 2):
        return True
    elif (not is_tile_black) and nb_black_neighbour == 2:
        return True

    return False


def do_one_round_of_tiles_change(dict_tiles):
    set_coords_tiles_to_flip = set()
    for coord, is_tile_black in dict_tiles.items():
        if does_this_tile_need_to_flip(dict_tiles, coord):
            set_coords_tiles_to_flip.add(coord)

        # if our tile is black, some tile never flipped may need a flip!
        if is_tile_black:
            list_neighbour_coordinates = compute_list_neighbours_coordinates(coord)
            for neighbour_coord in list_neighbour_coordinates:
                if does_this_tile_need_to_flip(dict_tiles, neighbour_coord):
                    set_coords_tiles_to_flip.add(neighbour_coord)

    for coord in set_coords_tiles_to_flip:
        dict_tiles[coord] = not dict_tiles[coord]


with open("data.txt") as f:
    content = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line

dict_flipped_tiles = collections.defaultdict(lambda: False)

for path_to_tile in content:
    dict_flipped_tiles[compute_str_coords_tile(path_to_tile)] = not dict_flipped_tiles[compute_str_coords_tile(path_to_tile)]

for _ in range(100):
    do_one_round_of_tiles_change(dict_flipped_tiles)

# 108 too low
print(sum(1 for value in dict_flipped_tiles.values() if value))
