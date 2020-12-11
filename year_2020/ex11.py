from copy import deepcopy


def safe_is_occupied_seat_present_at_coordinates(matrice_seats, line_num, col_num):
    if line_num < 0 or col_num < 0:
        return False
    try:
        return matrice_seats[line_num][col_num] == "#"
    except IndexError:
        return False


def count_occupied_seats_around_coordinates(matrice_seats, line_num, col_num):
    array_seats_occupied = [safe_is_occupied_seat_present_at_coordinates(matrice_seats, line_num - 1, col_num - 1)
        , safe_is_occupied_seat_present_at_coordinates(matrice_seats, line_num - 1, col_num)
        , safe_is_occupied_seat_present_at_coordinates(matrice_seats, line_num - 1, col_num + 1)
        , safe_is_occupied_seat_present_at_coordinates(matrice_seats, line_num, col_num - 1)
        , safe_is_occupied_seat_present_at_coordinates(matrice_seats, line_num, col_num + 1)
        , safe_is_occupied_seat_present_at_coordinates(matrice_seats, line_num + 1, col_num - 1)
        , safe_is_occupied_seat_present_at_coordinates(matrice_seats, line_num + 1, col_num)
        , safe_is_occupied_seat_present_at_coordinates(matrice_seats, line_num + 1, col_num + 1)]

    return array_seats_occupied.count(True)


def change_seats_matrice_while_changes_occur(seats_to_change):
    while True:
        has_at_least_one_changes_occured = False
        initial_seats = deepcopy(seats_to_change)

        for idx_line, line in enumerate(initial_seats):
            for idx_col, seat in enumerate(line):
                if seat != '.':
                    nb_occupied_seats = count_occupied_seats_around_coordinates(initial_seats, idx_line, idx_col)
                    if seat == 'L' and nb_occupied_seats == 0:
                        has_at_least_one_changes_occured = True
                        seats_to_change[idx_line][idx_col] = '#'
                    if seat == '#' and nb_occupied_seats >= 4:
                        has_at_least_one_changes_occured = True
                        seats_to_change[idx_line][idx_col] = 'L'

        if not has_at_least_one_changes_occured:
            break

    return seats_to_change


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line

array_seats = [list(x.strip()) for x in content]

final_array_seats = change_seats_matrice_while_changes_occur(array_seats)

occupied_seats = 0

for end_line in final_array_seats:
    occupied_seats += end_line.count('#')

# 2268 too high
print(occupied_seats)
