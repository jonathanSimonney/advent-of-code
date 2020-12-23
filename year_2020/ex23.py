def do_one_move(linked_dict_to_apply_move):
    removed_set_cups = set()

    # remove next 3 cups and keep them
    first_removed_cup_label = linked_dict_to_apply_move[current_cup_label]
    second_removed_cup_label = linked_dict_to_apply_move[first_removed_cup_label]
    third_removed_cup_label = linked_dict_to_apply_move[second_removed_cup_label]

    # chain of cups now goes from current to fourth cup
    linked_dict_to_apply_move[current_cup_label] = linked_dict_to_apply_move[third_removed_cup_label]

    removed_set_cups.add(first_removed_cup_label)
    removed_set_cups.add(second_removed_cup_label)
    removed_set_cups.add(third_removed_cup_label)

    # find a proper destination_number
    destination_number = current_cup_label - 1

    while destination_number in removed_set_cups or destination_number < 1:
        if destination_number < 1:
            destination_number = 1000001
            # destination_number = 10
        destination_number -= 1


    # append the elems removed right after the destination cup
    linked_dict_to_apply_move[third_removed_cup_label] = linked_dict_to_apply_move[destination_number]
    linked_dict_to_apply_move[destination_number] = first_removed_cup_label

    return linked_dict_to_apply_move[current_cup_label]


chain_cups = {
    1: 9,
    9: 8,
    8: 7,
    7: 5,
    5: 3,
    3: 4,
    4: 6,
    6: 2,
    2: 1
}

first_cup_label = 1
last_cup_label = 2

# chain_cups = {
#     3: 8,
#     8: 9,
#     9: 1,
#     1: 2,
#     2: 5,
#     5: 4,
#     4: 6,
#     6: 7,
#     7: 3
# }
#
# first_cup_label = 3
# last_cup_label = 7

label_to_add = 10
while len(chain_cups) != 1000000:
    chain_cups[last_cup_label] = label_to_add

    last_cup_label = label_to_add
    label_to_add += 1

chain_cups[last_cup_label - 1] = first_cup_label

# current_cup_label = 3
current_cup_label = 1

# for i in range(100):
for i in range(10000000):
    # print(f"-- move {i + 1} --")
    # print(chain_cups)
    current_cup_label = do_one_move(chain_cups)
    # if i % 1000 == 0:
    #     print(f"iteration number {i} done")

#42789356 too low
# print(chain_cups, current_cup_label)

# 6212592000 too low
# 695032060556 too high
print(chain_cups[1], chain_cups[chain_cups[1]])
print(chain_cups[1] * chain_cups[chain_cups[1]])
