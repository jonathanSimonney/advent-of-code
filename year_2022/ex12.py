import collections
import string
from typing import List, Set, Union, Optional, Dict

from common_helpers.position import Position, Traject

import sys
sys.setrecursionlimit(5000)

dict_positions_to_elevation: dict[Position, int] = {}
dict_positions_to_reachable_next_pos: dict[Position, List[Position]] = {}
dict_positions_to_reachable_from_pos: dict[Position, List[Position]] = {}


def compute_reachable_pos_from(position: Position) -> List[Position]:
    list_to_ret = []
    for target_pos in position.get_all_adjacent_pos_without_diagonal():
        try:
            if not dict_positions_to_elevation[target_pos] > dict_positions_to_elevation[position] + 1:
                list_to_ret.append(target_pos)
        except KeyError:
            continue
    return list_to_ret


def compute_reachable_pos_by(position: Position) -> List[Position]:
    list_to_ret = []

    # current pos can be reached from ANY adjacent pos 1 less height or more
    min_height_needed = dict_positions_to_elevation[position] - 1
    for target_pos in position.get_all_adjacent_pos_without_diagonal():
        try:
            if dict_positions_to_elevation[target_pos] >= min_height_needed:
                list_to_ret.append(target_pos)
        except KeyError:
            continue
    return list_to_ret


dict_shortcut_traject_cost: Dict[Position, Optional[int]] = {}


def fill_dict_costs(start_pos: Position, dict_reachable_pos: dict[Position, List[Position]]):
    dict_shortcut_traject_cost[start_pos] = 0
    rec_fill_adjacents_pos_costs(start_pos, 0, dict_reachable_pos)


def rec_fill_adjacents_pos_costs(pos: Position, cost_pos: int, dict_reachable_pos: dict[Position, List[Position]]):
    candidate_cost = cost_pos + 1

    for adjacent_pos in dict_reachable_pos[pos]:
        if adjacent_pos not in dict_shortcut_traject_cost or dict_shortcut_traject_cost[adjacent_pos] > candidate_cost:
            dict_shortcut_traject_cost[adjacent_pos] = candidate_cost
            rec_fill_adjacents_pos_costs(adjacent_pos, candidate_cost, dict_reachable_pos)


def main():
    with open("data.txt") as f:
        content = f.read().splitlines()

    global dict_positions_to_elevation
    global dict_positions_to_reachable_next_pos

    pos_start: Position
    pos_end: Position

    list_pos_elevation_0: List[Position] = []

    for x, line in enumerate(content):
        for y, letter in enumerate(line):
            if letter == 'S':
                elevation = 0
                pos_start = Position(x, y)
            elif letter == 'E':
                elevation = 25
                pos_end = Position(x, y)
            else:
                elevation = string.ascii_lowercase.index(letter.lower())
            dict_positions_to_elevation[Position(x, y)] = elevation
            if elevation == 0:
                list_pos_elevation_0.append(Position(x, y))

    for position in dict_positions_to_elevation.keys():
        dict_positions_to_reachable_next_pos[position] = compute_reachable_pos_from(position)
        dict_positions_to_reachable_from_pos[position] = compute_reachable_pos_by(position)

    print(dict_positions_to_reachable_next_pos[Position(2, 0)])
    print(pos_end)
    # fill_dict_costs(pos_start, dict_positions_to_reachable_next_pos)
    fill_dict_costs(pos_end, dict_positions_to_reachable_from_pos)

    # print(dict_shortcut_traject_cost[pos_end])
    min_cost = None
    for pos in list_pos_elevation_0:
        if pos in dict_shortcut_traject_cost:
            candidate_cost = dict_shortcut_traject_cost[pos]
            if min_cost is None or candidate_cost < min_cost:
                min_cost = candidate_cost

    print(min_cost)


if __name__ == "__main__":
    main()
