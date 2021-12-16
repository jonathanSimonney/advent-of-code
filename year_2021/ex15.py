from common_helpers.position import Position, print_ascii_with_set_position


def compute_more_accurate_travel_cost(dict_point_risk_level: dict, dict_point_travel_cost: dict) -> bool:
    has_change_occured = False
    for point, current_travel_cost in dict_point_travel_cost.items():
        list_adjacent_points_travel_costs: list[int] = [
            dict_point_travel_cost[adjacent_point] for adjacent_point in point.get_all_adjacent_pos_without_diagonal()
            if adjacent_point in dict_point_travel_cost
        ]
        candidate_travel_cost = min(list_adjacent_points_travel_costs) + dict_point_risk_level[point]
        if candidate_travel_cost < current_travel_cost:
            has_change_occured = True
            dict_point_travel_cost[point] = candidate_travel_cost

    return has_change_occured


def main():
    with open("data.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [line.strip() for line in content]

    dict_point_risk_level: dict = {}
    dict_point_travel_cost: dict = {}

    tile_y_length = len(content)
    tile_x_length = len(content[0])

    for y, line in enumerate(content):
        for x, char in enumerate(line):
            for y_tile_pos in range(5):
                for x_tile_pos in range(5):
                    dict_point_risk_level[
                        Position(x + x_tile_pos * tile_x_length, y + y_tile_pos * tile_y_length)
                    ] = (int(char) + x_tile_pos + y_tile_pos) % 9 or 9

    sum_risk_levels = 0
    max_y = len(content) * 5 - 1
    max_x = len(content[0]) * 5 - 1
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            sum_risk_levels += dict_point_risk_level[Position(x, y)]
            dict_point_travel_cost[Position(x, y)] = sum_risk_levels

    dict_point_travel_cost[Position(0, 0)] = 0
    should_i_continue = True
    while should_i_continue:
        should_i_continue = compute_more_accurate_travel_cost(dict_point_risk_level, dict_point_travel_cost)
        print("another loop ! ", dict_point_travel_cost[Position(max_x, max_y)])

    # print(dict_point_travel_cost)

    # 2864 too low
    # 2874 too high
    print(dict_point_travel_cost[Position(max_x, max_y)])
    # print(dict_point_travel_cost[Position(99, 99)])
    print(dict_point_travel_cost[Position(max_x - 1, max_y)])
    print(dict_point_travel_cost[Position(max_x, max_y - 1)])

    print(dict_point_travel_cost[Position(max_x - 1, max_y - 1)])
    print(dict_point_travel_cost[Position(max_x - 2, max_y)])
    print(dict_point_travel_cost[Position(max_x, max_y - 2)])
    print(compute_more_accurate_travel_cost(dict_point_risk_level, dict_point_travel_cost))


if __name__ == "__main__":
    main()

