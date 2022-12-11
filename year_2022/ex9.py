from dataclasses import dataclass
from typing import Set, List

from common_helpers.position import Direction, Position


@dataclass(frozen=True)
class Movement:
    nb_move: int
    direction: Direction


def parse_line_instruction(line_parsed: str) -> Movement:
    line_splitted = line_parsed.split(" ")
    dict_key_to_direction = {
        'R': Direction.RIGHT,
        'U': Direction.UP,
        'L': Direction.LEFT,
        'D': Direction.DOWN,
    }
    return Movement(int(line_splitted[1]), dict_key_to_direction[line_parsed[0]])


class System:
    head_rope_pos: Position
    list_rope_knots: List[Position]
    set_pos_visited_by_tail: Set[Position]

    def __init__(self):
        self.list_rope_knots = [Position(0, 0)] * 10
        self.set_pos_visited_by_tail = {Position(0, 0)}

    def move_head_in_direction(self, direction_movement: Direction):
        self.list_rope_knots[0] = self.list_rope_knots[0].get_pos_direction(direction_movement)
        for idx, knot in enumerate(self.list_rope_knots[1:]):
            self.list_rope_knots[idx + 1] = self.move_knot_following_position(self.list_rope_knots[idx], knot)
        self.set_pos_visited_by_tail.add(self.list_rope_knots[-1])

    @staticmethod
    def move_knot_following_position(knot_pos_to_follow: Position, knot_following_pos: Position) -> Position:
        if knot_following_pos == knot_pos_to_follow:
            print("first if")
            return knot_following_pos
        elif knot_following_pos.get_pos_direction_and_space(Direction.UP, 2) == knot_pos_to_follow:
            return knot_following_pos.get_pos_direction(Direction.UP)
        elif knot_following_pos.get_pos_direction_and_space(Direction.DOWN, 2) == knot_pos_to_follow:
            return knot_following_pos.get_pos_direction(Direction.DOWN)
        elif knot_following_pos.get_pos_direction_and_space(Direction.LEFT, 2) == knot_pos_to_follow:
            return knot_following_pos.get_pos_direction(Direction.LEFT)
        elif knot_following_pos.get_pos_direction_and_space(Direction.RIGHT, 2) == knot_pos_to_follow:
            return knot_following_pos.get_pos_direction(Direction.RIGHT)
        elif knot_pos_to_follow not in knot_following_pos.get_all_adjacent_pos():
            possible_pos = set(knot_pos_to_follow.get_all_adjacent_pos()).intersection(
                knot_following_pos.get_all_diagonal_pos()
            )
            if len(possible_pos) != 1:
                raise AssertionError("thought diagonal possible moves were LIMITED to one")
            return possible_pos.pop()
        return knot_following_pos


def main():
    with open("data.txt") as f:
        content = [parse_line_instruction(line) for line in f.read().splitlines()]

    system: System = System()

    # system.move_head_in_direction(Direction.RIGHT)
    # system.move_head_in_direction(Direction.UP)
    # system.move_head_in_direction(Direction.UP)

    # print(system.tail_rope_pos, system.head_rope_pos)

    for movement in content:
        for _ in range(movement.nb_move):
            system.move_head_in_direction(movement.direction)
    print(len(system.set_pos_visited_by_tail))


if __name__ == "__main__":
    main()
