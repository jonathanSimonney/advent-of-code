import collections


def count_active_cube_around_coordinates(dim_to_analyse, line_num, col_num, cote_num, time_num):
    nb_active_cubes = 0

    for x in range(line_num -1, line_num + 2):
        for y in range(col_num - 1, col_num + 2):
            for z in range(cote_num - 1, cote_num + 2):
                for t in range(time_num - 1, time_num + 2):
                    if x == line_num and y == col_num and z == cote_num and t == time_num:
                        continue
                    if dim_to_analyse[x][y][z][t] == '#':
                        nb_active_cubes += 1

    return nb_active_cubes


def expand_pocket_dim_by_n(pocket_dim_to_expand, size_to_expand_pocket_dim):
    pocket_dim_to_expand["min_coords"]["x"] -= size_to_expand_pocket_dim
    pocket_dim_to_expand["max_coords"]["x"] += size_to_expand_pocket_dim

    pocket_dim_to_expand["min_coords"]["y"] -= size_to_expand_pocket_dim
    pocket_dim_to_expand["max_coords"]["y"] += size_to_expand_pocket_dim

    pocket_dim_to_expand["min_coords"]["z"] -= size_to_expand_pocket_dim
    pocket_dim_to_expand["max_coords"]["z"] += size_to_expand_pocket_dim

    pocket_dim_to_expand["min_coords"]["t"] -= size_to_expand_pocket_dim
    pocket_dim_to_expand["max_coords"]["t"] += size_to_expand_pocket_dim


def change_pocket_dim_for_n_cycles(pocket_dim_with_infos, nb_cycles_to_execute):
    for _ in range(nb_cycles_to_execute):
        initial_dim = pocket_dim_with_infos["dimension"]
        expand_pocket_dim_by_n(pocket_dim_with_infos, 1)

        to_fill_pocket_dim = get_pocket_dim()

        for idx_line in range(pocket_dim_with_infos["min_coords"]["x"], pocket_dim_with_infos["max_coords"]["x"] + 1):
            for idx_col in range(pocket_dim_with_infos["min_coords"]["y"], pocket_dim_with_infos["max_coords"]["y"] + 1):
                for idx_cote in range(pocket_dim_with_infos["min_coords"]["z"], pocket_dim_with_infos["max_coords"]["z"] + 1):
                    for idx_time in range(pocket_dim_with_infos["min_coords"]["t"], pocket_dim_with_infos["max_coords"]["t"] + 1):
                        nb_active_cubes = count_active_cube_around_coordinates(initial_dim, idx_line, idx_col, idx_cote, idx_time)
                        cube_at_coords = initial_dim[idx_line][idx_col][idx_cote][idx_time]

                        if cube_at_coords == '#':
                            if 2 <= nb_active_cubes <= 3:
                                to_fill_pocket_dim[idx_line][idx_col][idx_cote][idx_time] = '#'
                            else:
                                to_fill_pocket_dim[idx_line][idx_col][idx_cote][idx_time] = '.'
                        elif nb_active_cubes == 3:
                            to_fill_pocket_dim[idx_line][idx_col][idx_cote][idx_time] = '#'

        pocket_dim_with_infos["dimension"] = to_fill_pocket_dim


def create_new_line_dict():
    return collections.defaultdict(lambda: '.')


def create_new_col_dict():
    return collections.defaultdict(lambda: create_new_line_dict())


def create_new_additional_dim_dict():
    return collections.defaultdict(lambda: create_new_col_dict())


def get_pocket_dim():
    return collections.defaultdict(lambda: create_new_additional_dim_dict())


def debug_print_pocket(dict_pocket_to_print):
    for z in range(pocket_dimension_dict["min_coords"]["z"], pocket_dimension_dict["max_coords"]["z"] + 1):
        print(f"z={z}")
        str_to_print = ""

        for x in range(pocket_dimension_dict["min_coords"]["x"], pocket_dimension_dict["max_coords"]["x"] + 1):
            for y in range(pocket_dimension_dict["min_coords"]["y"], pocket_dimension_dict["max_coords"]["y"] + 1):
                str_to_print += dict_pocket_to_print["dimension"][x][y][z]
            str_to_print += "\n"
        print(str_to_print)


with open("data.txt") as f:
    content = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line

pocket_dimension = get_pocket_dim()
pocket_dimension_dict = {
    "dimension": pocket_dimension,
    "min_coords": {"x": 0, "y": 0, "z": 0, "t": 0},
    "max_coords": {"x": -1, "y": 0, "z": 0, "t": 0}
}

for x, str_cubes in enumerate(content):
    pocket_dimension_dict["max_coords"]["x"] += 1
    pocket_dimension_dict["max_coords"]["y"] = len(str_cubes) - 1
    for y, cube in enumerate(str_cubes):
        pocket_dimension[x][y][0][0] = cube

change_pocket_dim_for_n_cycles(pocket_dimension_dict, 6)

nb_active_cubes = 0


for idx_line in range(pocket_dimension_dict["min_coords"]["x"], pocket_dimension_dict["max_coords"]["x"] + 1):
    for idx_col in range(pocket_dimension_dict["min_coords"]["y"], pocket_dimension_dict["max_coords"]["y"] + 1):
        for idx_cote in range(pocket_dimension_dict["min_coords"]["z"], pocket_dimension_dict["max_coords"]["z"] + 1):
            for idx_time in range(pocket_dimension_dict["min_coords"]["t"], pocket_dimension_dict["max_coords"]["t"] + 1):
                if pocket_dimension_dict["dimension"][idx_line][idx_col][idx_cote][idx_time] == '#':
                    nb_active_cubes += 1

# 3105 too high
print(nb_active_cubes)

# debug_print_pocket(pocket_dimension_dict)
