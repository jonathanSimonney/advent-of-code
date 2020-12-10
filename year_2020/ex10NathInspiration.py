from functools import lru_cache


@lru_cache(maxsize=None)
def count_all_possibilities(joltage_to_lookup):
    nb_pos = 1 if dict_joltage_reachable[joltage_to_lookup] == [] else 0
    for joltage_in_dict in dict_joltage_reachable[joltage_to_lookup]:
        nb_pos += count_all_possibilities(joltage_in_dict)

    return nb_pos


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line

array_int = sorted([int(x.strip()) for x in content])

dict_joltage_reachable = {}
list_joltage_diff = []
old_joltage = 0
array_int.insert(0, 0)
for joltage in array_int:
    list_joltage_diff.append(joltage - old_joltage)
    old_joltage = joltage

    current_iter_joltage_reachable = []
    for i in range(3):
        if joltage + i + 1 in array_int:
            current_iter_joltage_reachable.append(joltage + i + 1)

    dict_joltage_reachable[joltage] = current_iter_joltage_reachable

# built in adapter always 3 higher than my max joltage in list
list_joltage_diff.append(3)
print(list_joltage_diff.count(3) * list_joltage_diff.count(1))

print(count_all_possibilities(0))
