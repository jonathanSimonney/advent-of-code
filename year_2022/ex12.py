import string
from typing import List, Set, Union, Optional

from common_helpers.position import Position


dict_positions_to_elevation: dict[Position, int] = {}
dict_positions_to_reachable_next_pos: dict[Position, List[Position]] = {}


def compute_reachable_pos_from(position: Position) -> List[Position]:
    list_to_ret = []
    for target_pos in position.get_all_adjacent_pos_without_diagonal():
        try:
            if not dict_positions_to_elevation[target_pos] > dict_positions_to_elevation[position] + 1:
                list_to_ret.append(target_pos)
        except KeyError:
            continue
    return list_to_ret


def find_shortest_path_len_between_pos(
        start: Position,
        end: Position,
        set_visited_pos: Set[Position] = None
) -> Optional[int]:
    if set_visited_pos is None:
        set_visited_pos: Set[Position] = {start}
    if start == end:
        return 0
    best_solution: Optional[int] = None
    for pos in dict_positions_to_reachable_next_pos[start]:
        if pos not in set_visited_pos:
            set_visited_pos.add(pos)
            possible_solution = find_shortest_path_len_between_pos(pos, end, set_visited_pos)
            if possible_solution is not None and (best_solution is None or best_solution > possible_solution + 1):
                print(possible_solution)
                best_solution = possible_solution + 1
            set_visited_pos.remove(pos)
    return best_solution


def main():
    with open("data.txt") as f:
        content = f.read().splitlines()

    global dict_positions_to_elevation
    global dict_positions_to_reachable_next_pos

    pos_start: Position
    pos_end: Position

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

    for position in dict_positions_to_elevation.keys():
        dict_positions_to_reachable_next_pos[position] = compute_reachable_pos_from(position)

    print(find_shortest_path_len_between_pos(pos_start, pos_end))


if __name__ == "__main__":
    main()
