def move_element_in_direction(element_info_param, direction_to_move, value_to_move):
    if direction_to_move == 'N':
        element_info_param["y_pos"] += value_to_move
    elif direction_to_move == 'S':
        element_info_param["y_pos"] -= value_to_move
    elif direction_to_move == 'E':
        element_info_param["x_pos"] += value_to_move
    elif direction_to_move == 'W':
        element_info_param["x_pos"] -= value_to_move


def move_waypoint_right(waypoint_pos):
    base_x = waypoint_pos["x_pos"]
    base_y = waypoint_pos["y_pos"]
    waypoint_pos["x_pos"] = base_y
    waypoint_pos["y_pos"] = -base_x


def move_waypoint_left(waypoint_pos):
    base_x = waypoint_pos["x_pos"]
    base_y = waypoint_pos["y_pos"]
    waypoint_pos["x_pos"] = -base_y
    waypoint_pos["y_pos"] = base_x


def move_ship_with_instruction(ship_info_param, instruction):
    instruction_action = instruction[0]
    instruction_value = int(instruction[1:])

    if instruction_action == 'L':
        nb_times_to_move_waypoint = int(instruction_value / 90)
        for i in range(nb_times_to_move_waypoint):
            move_waypoint_left(ship_info_param["waypoint_infos"])
    elif instruction_action == 'R':
        nb_times_to_move_waypoint = int(instruction_value / 90)
        for i in range(nb_times_to_move_waypoint):
            move_waypoint_right(ship_info_param["waypoint_infos"])
    elif instruction_action == 'F':
        ship_info_param["x_pos"] += instruction_value * ship_info_param["waypoint_infos"]["x_pos"]
        ship_info_param["y_pos"] += instruction_value * ship_info_param["waypoint_infos"]["y_pos"]
    else:
        move_element_in_direction(ship_info_param["waypoint_infos"], instruction_action, instruction_value)


with open("data.txt") as f:
    list_instruction = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line

ship_info = {"x_pos": 0, "y_pos": 0, "waypoint_infos": {"x_pos": 10, "y_pos": 1}}

for instruction_str in list_instruction:
    move_ship_with_instruction(ship_info, instruction_str)

#2179 too high
print(abs(ship_info["x_pos"]) + abs(ship_info["y_pos"]))
