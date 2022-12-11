from dataclasses import dataclass
from typing import Set

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
    tail_rope_pos: Position
    set_pos_visited_by_tail: Set[Position]

    def __init__(self):
        self.head_rope_pos = Position(0, 0)
        self.tail_rope_pos = Position(0, 0)
        self.set_pos_visited_by_tail = {self.head_rope_pos}

    def move_head_in_direction(self, direction_movement: Direction):
        self.head_rope_pos = self.head_rope_pos.get_pos_direction(direction_movement)
        if self.tail_rope_pos == self.head_rope_pos:
            pass
        elif self.tail_rope_pos.get_pos_direction_and_space(Direction.UP, 2) == self.head_rope_pos:
            self.tail_rope_pos = self.tail_rope_pos.get_pos_direction(Direction.UP)
        elif self.tail_rope_pos.get_pos_direction_and_space(Direction.DOWN, 2) == self.head_rope_pos:
            self.tail_rope_pos = self.tail_rope_pos.get_pos_direction(Direction.DOWN)
        elif self.tail_rope_pos.get_pos_direction_and_space(Direction.LEFT, 2) == self.head_rope_pos:
            self.tail_rope_pos = self.tail_rope_pos.get_pos_direction(Direction.LEFT)
        elif self.tail_rope_pos.get_pos_direction_and_space(Direction.RIGHT, 2) == self.head_rope_pos:
            self.tail_rope_pos = self.tail_rope_pos.get_pos_direction(Direction.RIGHT)
        elif self.head_rope_pos not in self.tail_rope_pos.get_all_adjacent_pos():
            possible_pos = set(self.head_rope_pos.get_all_adjacent_pos()).intersection(
                self.tail_rope_pos.get_all_diagonal_pos()
            )
            if len(possible_pos) != 1:
                print(possible_pos)
                print(self.head_rope_pos, self.tail_rope_pos)
                raise AssertionError("thought diagonal possible moves were LIMITED to one")
            self.tail_rope_pos = possible_pos.pop()

        self.set_pos_visited_by_tail.add(self.tail_rope_pos)


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
