from common_helpers.position import Position


octopus_min_energy_needed_to_flash: int = 10


def simulate_one_step(dict_octopuses_pos_to_energy: dict) -> int:
    nb_flash_occured = 0
    set_flashed_pos: set[Position] = set()
    list_pos_to_flash: list[Position] = []

    for key in dict_octopuses_pos_to_energy.keys():
        if key in dict_octopuses_pos_to_energy:
            dict_octopuses_pos_to_energy[key] += 1
            if dict_octopuses_pos_to_energy[key] == octopus_min_energy_needed_to_flash:
                list_pos_to_flash.append(key)

    while True:
        next_iteration_list_pos_to_flash = []
        for pos in list_pos_to_flash:
            nb_flash_occured += 1
            set_flashed_pos.add(pos)
            for adjacent_pos in pos.get_all_adjacent_pos():
                if adjacent_pos in dict_octopuses_pos_to_energy:
                    dict_octopuses_pos_to_energy[adjacent_pos] += 1
                    if dict_octopuses_pos_to_energy[adjacent_pos] == octopus_min_energy_needed_to_flash:
                        next_iteration_list_pos_to_flash.append(adjacent_pos)
        if len(next_iteration_list_pos_to_flash) != 0:
            list_pos_to_flash = next_iteration_list_pos_to_flash
        else:
            break

    for pos_to_reset in set_flashed_pos:
        dict_octopuses_pos_to_energy[pos_to_reset] = 0
    return nb_flash_occured


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [[int(char) for char in line.strip()] for line in content]

dict_positions: dict = {}

for x, line in enumerate(content):
    for y, energy_level in enumerate(line):
        dict_positions[Position(x, y)] = energy_level


# accumulator: int = 0
#
# for _ in range(100):
#     accumulator += simulate_one_step(dict_positions)
# # 1815 too high
# print(accumulator)

nb_step_occured = 0
while True:
    nb_step_occured += 1
    nb_flash_occured = simulate_one_step(dict_positions)
    if nb_flash_occured == 100:
        break

print(nb_step_occured)

