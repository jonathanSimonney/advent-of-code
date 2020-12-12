def move_ship_in_direction(ship_info_param, direction_to_move, value_to_move):
    if direction_to_move == 'N':
        ship_info_param["y_pos"] += value_to_move
    elif direction_to_move == 'S':
        ship_info_param["y_pos"] -= value_to_move
    elif direction_to_move == 'E':
        ship_info_param["x_pos"] += value_to_move
    elif direction_to_move == 'W':
        ship_info_param["x_pos"] -= value_to_move


def move_ship_with_instruction(ship_info_param, instruction):
    instruction_action = instruction[0]
    instruction_value = int(instruction[1:])

    if instruction_action == 'L':
        ship_info_param["current_facing_index"] = (ship_info_param["current_facing_index"] - int(instruction_value / 90)) % 4
    elif instruction_action == 'R':
        ship_info_param["current_facing_index"] = (int(instruction_value / 90) + ship_info_param["current_facing_index"]) % 4
    elif instruction_action == 'F':
        move_ship_in_direction(ship_info_param, tuple_directions[ship_info_param["current_facing_index"]], instruction_value)
    else:
        move_ship_in_direction(ship_info_param, instruction_action, instruction_value)


with open("data.txt") as f:
    list_instruction = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line

tuple_directions = ('E', 'S', 'W', 'N')

ship_info = {"x_pos": 0, "y_pos": 0, "current_facing_index": 0}

for instruction_str in list_instruction:
    move_ship_with_instruction(ship_info, instruction_str)

#2179 too high
print(abs(ship_info["x_pos"]) + abs(ship_info["y_pos"]))
