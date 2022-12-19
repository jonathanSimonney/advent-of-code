from typing import List, Union, Optional, Set
import sys

from common_helpers.position import Position
from common_helpers.range_helper import create_inclusive_range_properly_ordered


class System:
    set_rock_pos: Set[Position] = set()
    set_sand_pos: Set[Position] = set()
    _last_sand_grain_forelast_pos: Optional[Position] = None
    abyss_ceiling_y: Optional[int] = None

    def make_grain_fall_until_abyss(self):
        pass

    # will return True if grain went to rest, False if it ended in the abyss,
    def _make_grain_fall(self) -> bool:
        if self._last_sand_grain_forelast_pos is None:
            self._last_sand_grain_forelast_pos = Position(500, 0)
        next_pos = self._compute_next_valid_pos_from(self._last_sand_grain_forelast_pos)
        while next_pos is not False and next_pos.y < self.abyss_ceiling_y:
            self._last_sand_grain_forelast_pos = next_pos
            next_pos = self._compute_next_valid_pos_from(self._last_sand_grain_forelast_pos)

        if next_pos.y >= self.abyss_ceiling_y:
            return False

        # come back here to ensure the grain fall logic is ok
        self.set_sand_pos.add(next_pos)


    # will return false if no valid next pos is available
    def _compute_next_valid_pos_from(self, from_pos: Position) -> Union[Position, False]:
        candidate_pos = from_pos.get_bottom_pos()
        if not self._is_pos_occupied(candidate_pos):
            return candidate_pos
        candidate_pos = from_pos.get_bottom_left_pos()
        if not self._is_pos_occupied(candidate_pos):
            return candidate_pos
        candidate_pos = from_pos.get_bottom_right_pos()
        if not self._is_pos_occupied(candidate_pos):
            return candidate_pos

        return False

    def _is_pos_occupied(self, pos_param: Position) -> bool:
        if pos_param in self.set_rock_pos or pos_param in self.set_sand_pos:
            return True
        return False

    def add_segment_rock_from_to(self, pos_start: Position, pos_end: Position):
        if pos_start.x == pos_end.x:
            for y in create_inclusive_range_properly_ordered(pos_start.y, pos_end.y):
                self.set_rock_pos.add(Position(pos_start.x, y))
        elif pos_start.y == pos_end.y:
            for x in create_inclusive_range_properly_ordered(pos_start.x, pos_end.x):
                self.set_rock_pos.add(Position(x, pos_start.y))
        else:
            raise AssertionError("pos start and pos end should have either x or y be the same")


def parse_line_in_system(line: str, system: System):
    list_pos = line.split(' -> ')

    pos_dataclass_former: Optional[Position] = None
    max_y_found = system.abyss_ceiling_y

    for pos_str in list_pos:
        pos_split = pos_str.split(',')
        pos_dataclass = Position(int(pos_split[0]), int(pos_split[1]))

        candidate_y = pos_dataclass.y
        if max_y_found is None or candidate_y > max_y_found:
            max_y_found = candidate_y

        if pos_dataclass_former is not None:
            system.add_segment_rock_from_to(pos_dataclass_former, pos_dataclass)

        pos_dataclass_former = pos_dataclass

    candidate_y = pos_dataclass_former.y
    if max_y_found is None or candidate_y > max_y_found:
        max_y_found = candidate_y

    system.abyss_ceiling_y = max_y_found


def main():
    with open("data.txt") as f:
        content = f.read().splitlines()
    system = System()

    for line in content:
        parse_line_in_system(line, system)

    # system.make_grain_fall_until_abyss()

    print(len(system.set_sand_pos))
    print(system.abyss_ceiling_y)


if __name__ == "__main__":
    main()
