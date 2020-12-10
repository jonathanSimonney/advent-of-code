# as long as we're at 3 or below, a new possible value means double possibilities (keep existing ones, and add newer
# value to all of them) once we pass the third value, a new value will still need to remove 1 value, the one where the
# treshold was already 3 (and would therefore become higher). Further calculation for list possible values if you need
# to be more convinced:
# 1: 1
# 2: 2
# 3: 4
# 4: 7
# 5: 13

# the reason for this is a list of 5 elems means we could either do :
# possibilities for 4 as last with the 5 added
# 1, 2, 3, 4, 5
# 1, 3, 4, 5
# 1, 2, 4, 5
# 1, 4, 5
# 2, 3, 4, 5
# 2, 4, 5
# 3, 4, 5
 # same as just before, with the 4 removed as it's not anymore a mandatory last val
# 1, 2, 3, 5
# 1, 3, 5
# 1, 2, 5
# 1, 5 invalid!
# 2, 3, 5
# 2, 5
# 3, 5
def count_possible_arrangement_for_list_ones(nb_ones):
    nb_arrangement = 1
    # -1 as we need to start at 1 to multiply efficiently, so first elem shouldn't be counted
    for i in range(nb_ones - 1):
        nb_arrangement *= 2
        if i > 1:
            nb_arrangement -= 1

    return nb_arrangement


def count_all_possibilities(ordered_list_joltage_diff):
    copied_list = ordered_list_joltage_diff.copy()
    nb_possibilities = 1
    is_currently_iterating_over_ones = True if copied_list[0] == 1 else False
    current_iter_nb_possibilities = 0

    try:
        while True:
            value_to_find = 1 if is_currently_iterating_over_ones else 3
            if copied_list[0] == value_to_find:
                current_iter_nb_possibilities += 1
                copied_list.pop(0)
            else:
                if is_currently_iterating_over_ones:
                    nb_possibilities *= count_possible_arrangement_for_list_ones(current_iter_nb_possibilities)
                is_currently_iterating_over_ones = not is_currently_iterating_over_ones
                current_iter_nb_possibilities = 0
    except IndexError:
        return nb_possibilities


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line

array_int = sorted([int(x.strip()) for x in content])

list_joltage_diff = []
old_joltage = 0
for joltage in array_int:
    list_joltage_diff.append(joltage - old_joltage)
    old_joltage = joltage

# built in adapter always 3 higher than my max joltage in list
list_joltage_diff.append(3)
print(list_joltage_diff.count(3) * list_joltage_diff.count(1))


print(list_joltage_diff)
print(count_all_possibilities(list_joltage_diff))
