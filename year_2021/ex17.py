import collections


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
            # return range_nb_to_ret
        x_velocity -= 1

    if len(range_nb_to_ret) != 0:
        # return range_nb_to_ret
        return {'range_valid': range_nb_to_ret, 'is_last_one_always_within': True}
    # return [-1]
    return {'range_valid': [-1], 'is_last_one_always_within': False}


def compute_nb_step_to_be_in_target_area_y_range(y_velocity: int) -> list[int]:
    start_y = 0
    nb_steps_taken = 0
    range_nb_to_ret = []
    while start_y > min_y:
        nb_steps_taken += 1
        start_y += y_velocity
        y_velocity -= 1
        if start_y in target_area_y_range:
            range_nb_to_ret.append(nb_steps_taken)
    return range_nb_to_ret


def main():
    nb_next_invalid_needed_to_stop = 1000
    result_highest_y = 0

    dict_x_vel_valid_forever_to_min_steps_needed: dict = {}
    dict_step_to_valid_initial_velocities = collections.defaultdict(lambda: {'x_vel': [], 'y_vel': []})
    for x in range(max_x + 1):
        range_nb_step_for_valid_x = compute_nb_step_to_be_in_target_area_x_range(x)
        if range_nb_step_for_valid_x['is_last_one_always_within']:
            dict_x_vel_valid_forever_to_min_steps_needed[x] = range_nb_step_for_valid_x['range_valid'][0]
        else:
            for nb_step in range_nb_step_for_valid_x['range_valid']:
                dict_step_to_valid_initial_velocities[nb_step]['x_vel'].append(x)

    tested_y = min_y - 1
    nb_invalid = 0
    while nb_invalid < nb_next_invalid_needed_to_stop:
        tested_y += 1
        range_nb_step_for_valid_y = compute_nb_step_to_be_in_target_area_y_range(tested_y)
        if not range_nb_step_for_valid_y:
            nb_invalid += 1
        for nb_step in range_nb_step_for_valid_y:
            dict_step_to_valid_initial_velocities[nb_step]['y_vel'].append(tested_y)
            if not dict_step_to_valid_initial_velocities[nb_step]['x_vel']:
                nb_invalid += 1
            else:
                nb_invalid = 0

    set_dictinct_velocities: set = set()
    for nb_step, elem in dict_step_to_valid_initial_velocities.items():
        for x_vel, min_step_needed in dict_x_vel_valid_forever_to_min_steps_needed.items():
            if nb_step >= min_step_needed:
                elem['x_vel'].append(x_vel)

        if elem['x_vel'] and elem['y_vel'] and max(elem['y_vel']) > result_highest_y:
            result_highest_y = max(elem['y_vel'])

        for y_vel in elem['y_vel']:
            for x_vel in elem['x_vel']:
                set_dictinct_velocities.add(f'{x_vel}{y_vel}')

    print(result_highest_y)
    # 2628 too low
    print(result_highest_y * (result_highest_y + 1) / 2)
    # 4542 too low
    print(len(set_dictinct_velocities))


if __name__ == "__main__":
    main()
