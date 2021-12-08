import collections


dict_alignment_cost_per_distance = {0: 0}


def compute_cost_move_of_distance(move_length: int) -> int:
    if move_length not in dict_alignment_cost_per_distance:
        dict_alignment_cost_per_distance[move_length] = compute_cost_move_of_distance(move_length - 1) + move_length
    return dict_alignment_cost_per_distance[move_length]


def compute_cost_alignment_on_pos(dict_nb_crabs_on_pos: dict, pos_tested: int) -> int:
    total_cost = 0
    for init_pos, nb_crabs_on_pos in dict_nb_crabs_on_pos.items():
        key_alignment_cost = abs(pos_tested - init_pos)
        if key_alignment_cost not in dict_alignment_cost_per_distance:
            dict_alignment_cost_per_distance[key_alignment_cost] = compute_cost_move_of_distance(key_alignment_cost)
        total_cost += nb_crabs_on_pos * dict_alignment_cost_per_distance[key_alignment_cost]
    return total_cost


with open("data.txt") as f:
    content = f.readlines()[0].split(',')
# you may also want to remove whitespace characters like `\n` at the end of each line
content = sorted(int(x) for x in content)

dict_content = collections.defaultdict(lambda: 0)
for horizontal_pos in content:
    dict_content[horizontal_pos] += 1
print(dict_content)

dict_alignment_cost: dict = {}

previous_iteration_key = None
previous_pos_sum = 0
future_pos_sum = sum(dict_content.values())
for key in range(max(dict_content.keys())):
    dict_alignment_cost[key] = compute_cost_alignment_on_pos(dict_content, key)

print(min(dict_alignment_cost.values()))
