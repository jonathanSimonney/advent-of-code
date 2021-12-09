from common_helpers.position import Position


def is_single_pos_in_bassin(dict_positions_to_height: dict,
                            pos_in_bassin: Position,
                            candidate_pos: Position) -> bool:
    return candidate_pos in dict_positions_to_height \
           and dict_positions_to_height[candidate_pos] > dict_positions_to_height[pos_in_bassin] \
           and dict_positions_to_height[candidate_pos] != 9


def get_full_bassin_len_rec(dict_positions_to_height: dict,
                            starting_pos_to_check: Position,
                            set_already_found_points=None,
                            current_len_bassin=1) -> int:
    if set_already_found_points is None:
        set_already_found_points: set[Position] = {starting_pos_to_check}
    pos_to_right = starting_pos_to_check.get_right_pos()
    pos_to_left = starting_pos_to_check.get_left_pos()
    pos_to_top = starting_pos_to_check.get_top_pos()
    pos_to_bottom = starting_pos_to_check.get_bottom_pos()

    if pos_to_right not in set_already_found_points \
            and is_single_pos_in_bassin(dict_positions_to_height, starting_pos_to_check, pos_to_right):
        set_already_found_points.add(pos_to_right)
        current_len_bassin = get_full_bassin_len_rec(
            dict_positions_to_height,
            pos_to_right,
            set_already_found_points,
            current_len_bassin + 1
        )

    if pos_to_left not in set_already_found_points \
            and is_single_pos_in_bassin(dict_positions_to_height, starting_pos_to_check, pos_to_left):
        set_already_found_points.add(pos_to_left)
        current_len_bassin = get_full_bassin_len_rec(
            dict_positions_to_height,
            pos_to_left,
            set_already_found_points,
            current_len_bassin + 1
        )

    if pos_to_top not in set_already_found_points \
            and is_single_pos_in_bassin(dict_positions_to_height, starting_pos_to_check, pos_to_top):
        set_already_found_points.add(pos_to_top)
        current_len_bassin = get_full_bassin_len_rec(
            dict_positions_to_height,
            pos_to_top,
            set_already_found_points,
            current_len_bassin + 1
        )

    if pos_to_bottom not in set_already_found_points \
            and is_single_pos_in_bassin(dict_positions_to_height, starting_pos_to_check, pos_to_bottom):
        set_already_found_points.add(pos_to_bottom)
        current_len_bassin = get_full_bassin_len_rec(
            dict_positions_to_height,
            pos_to_bottom,
            set_already_found_points,
            current_len_bassin + 1
        )

    return current_len_bassin



with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [[int(char) for char in line.strip()] for line in content]

dict_positions: dict = {}

for x, line in enumerate(content):
    for y, height in enumerate(line):
        dict_positions[Position(x, y)] = height

list_bassin_length: list[int] = []
for x, line in enumerate(content):
    for y, height in enumerate(line):
        pos_to_check = Position(x, y)
        pos_to_right = pos_to_check.get_right_pos()
        pos_to_left = pos_to_check.get_left_pos()
        pos_to_top = pos_to_check.get_top_pos()
        pos_to_bottom = pos_to_check.get_bottom_pos()
        if (pos_to_right not in dict_positions or dict_positions[pos_to_right] > height) \
                and (pos_to_left not in dict_positions or dict_positions[pos_to_left] > height) \
                and (pos_to_top not in dict_positions or dict_positions[pos_to_top] > height) \
                and (pos_to_bottom not in dict_positions or dict_positions[pos_to_bottom] > height):
            list_bassin_length.append(get_full_bassin_len_rec(dict_positions, pos_to_check))

list_bassin_length.sort()
# 1404223614 too high
print(list_bassin_length[-1] * list_bassin_length[-2] * list_bassin_length[-3])
