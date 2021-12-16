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

    set_point_pos: set[Position] = set()

    dict_point_risk_level: dict = {}
    dict_point_travel_cost: dict = {}

    sum_risk_levels = 0

    for y, line in enumerate(content):
        for x, char in enumerate(line):
            dict_point_risk_level[Position(x, y)] = int(char)
            sum_risk_levels += int(char)
            dict_point_travel_cost[Position(x, y)] = sum_risk_levels

    dict_point_travel_cost[Position(0, 0)] = 0
    are_travel_cost_accurate = False
    while not are_travel_cost_accurate:
        are_travel_cost_accurate = compute_more_accurate_travel_cost(dict_point_risk_level, dict_point_travel_cost)

    print(dict_point_travel_cost)

    max_y = len(content) - 1
    max_x = len(content[0]) - 1
    print(dict_point_travel_cost[Position(max_x, max_y)])


if __name__ == "__main__":
    main()

