min_y = -148
max_y = -89
min_x = 139
max_x = 187

# min_y = -10
# max_y = -5
# min_x = 20
# max_x = 30
target_area_x_range = range(min_x, max_x + 1)
target_area_y_range = range(min_y, max_y + 1)


# this method returns [-1] if the probe never reaches target area x range
def compute_nb_step_to_be_in_target_area_x_range(x_velocity: int) -> dict:
    start_x = 0
    nb_steps = 0
    range_nb_to_ret = []
    while x_velocity != 0:
        nb_steps += 1
        start_x += x_velocity
        if start_x in target_area_x_range:
            range_nb_to_ret.append(nb_steps)
        elif len(range_nb_to_ret) != 0:
            return {'range_valid': range_nb_to_ret, 'is_last_one_always_within': False}
        x_velocity -= 1

    if len(range_nb_to_ret) != 0:
        return {'range_valid': range_nb_to_ret, 'is_last_one_always_within': True}
    return {'range_valid': [-1]}


def is_y_in_target_area_y_range_during_n_steps(y_velocity: int, nb_steps: dict) -> bool:
    start_y = 0
    nb_steps_taken = 0
    while start_y > min_y:
        nb_steps_taken += 1
        start_y += y_velocity
        y_velocity -= 1
        if start_y in target_area_y_range and \
                (nb_steps_taken in nb_steps['range_valid']
                 or
                 (nb_steps['is_last_one_always_within'] and nb_steps_taken >= nb_steps['range_valid'][-1])
                ):
            return True
    return False


def main():
    nb_next_invalid_needed_to_stop = 100
    result_highest_y = 0
    for x in range(max_x):
        range_nb_step_for_valid_x = compute_nb_step_to_be_in_target_area_x_range(x)
        if range_nb_step_for_valid_x['range_valid'] != [-1]:
            tested_y = 0
            nb_invalid = 0
            while nb_invalid < nb_next_invalid_needed_to_stop:
                tested_y += 1
                if is_y_in_target_area_y_range_during_n_steps(tested_y, range_nb_step_for_valid_x):
                    nb_invalid = 0
                    if tested_y > result_highest_y:
                        result_highest_y = tested_y
                else:
                    nb_invalid += 1

#2628 too low
    print(result_highest_y * (result_highest_y + 1) / 2)
    print(compute_nb_step_to_be_in_target_area_x_range(6))


if __name__ == "__main__":
    main()

