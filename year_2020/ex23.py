def do_one_move(list_cups_to_apply_move):
    removed_list_cups = []
    next_list_cups = []
    current_cup_number = list_cups_to_apply_move[current_cup_index]

    # remove next 3 cups and keep them
    first_removed_cup_label = list_cups_to_apply_move[(current_cup_index + 1) % 9]
    second_removed_cup_label = list_cups_to_apply_move[(current_cup_index + 2) % 9]
    third_removed_cup_label = list_cups_to_apply_move[(current_cup_index + 3) % 9]
    # print(f"pick up: {first_removed_cup_label}, {second_removed_cup_label}, {third_removed_cup_label}")

    removed_list_cups.append(first_removed_cup_label)
    removed_list_cups.append(second_removed_cup_label)
    removed_list_cups.append(third_removed_cup_label)

    list_cups_to_apply_move.remove(first_removed_cup_label)
    list_cups_to_apply_move.remove(second_removed_cup_label)
    list_cups_to_apply_move.remove(third_removed_cup_label)

    # find a proper destination_number
    destination_number = current_cup_number - 1

    while destination_number not in list_cups_to_apply_move:
        if destination_number < 1:
            destination_number = 10
        destination_number -= 1

    # print(f"destination: {destination_number}")

    # append the elems removed right after the destination cup
    for cup_label in list_cups_to_apply_move:
        next_list_cups.append(cup_label)
        if cup_label == destination_number:
            next_list_cups.extend(removed_list_cups)

    # find the next cup index
    for idx_cup, cup_label in enumerate(next_list_cups):
        if cup_label == current_cup_number:
            next_current_cup_index = (idx_cup + 1) % 9

    return {"list_cups": next_list_cups, "index_current": next_current_cup_index}


list_cups = [1, 9, 8, 7, 5, 3, 4, 6, 2]
# list_cups = [3, 8, 9, 1, 2, 5, 4, 6, 7]
current_cup_index = 0

for i in range(100):
    # current_cup_label = list_cups[current_cup_index]
    # print(f"-- move {i + 1} --")
    # print(f"cups: {['(' + str(x) + ')' if x == current_cup_label else str(x) for x in list_cups]}")
    result_move = do_one_move(list_cups)
    list_cups = result_move["list_cups"]
    current_cup_index = result_move["index_current"]

#42789356 too low
print(list_cups, current_cup_index)
