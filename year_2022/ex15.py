import collections
import re
import time
from typing import List, Optional, Dict

from common_helpers.position import Position
from common_helpers.range_helper import range_overlap, create_inclusive_range_properly_ordered


min_pos: int = 0
max_pos: int = 4000000


class Sensor:
    sensor_pos: Position
    closest_beacon_pos: Position
    _manhattan_dist: int

    def get_range_pos_without_beacon_on_line(self, y: int) -> Optional[range]:
        y_part_manhattan_dist = abs(self.sensor_pos.y - y)
        x_part_manhattan_dist_needed = self._manhattan_dist - y_part_manhattan_dist
        if x_part_manhattan_dist_needed < 0:
            # print(f"no useful info from sensor ar ")
            return None

        x_range_lower = self.sensor_pos.x - x_part_manhattan_dist_needed
        x_range_upper = self.sensor_pos.x + x_part_manhattan_dist_needed
        if self.closest_beacon_pos.y == y:
            if self.closest_beacon_pos.x == x_range_lower:
                x_range_lower += 1
            else:
                x_range_upper -= 1
        return range(max(x_range_lower, min_pos), min(x_range_upper, max_pos) + 1)

    def get_range_pos_without_beacon_on_column(self, x: int) -> Optional[range]:
        x_part_manhattan_dist = abs(self.sensor_pos.x - x)
        y_part_manhattan_dist_needed = self._manhattan_dist - x_part_manhattan_dist
        if y_part_manhattan_dist_needed < 0:
            # print(f"no useful info from sensor ar ")
            return None

        y_range_lower = self.sensor_pos.y - y_part_manhattan_dist_needed
        y_range_upper = self.sensor_pos.y + y_part_manhattan_dist_needed
        if self.closest_beacon_pos.x == x:
            if self.closest_beacon_pos.y == y_range_lower:
                y_range_lower += 1
            else:
                y_range_upper -= 1
        return range(max(y_range_lower, min_pos), min(y_range_upper, max_pos) + 1)

    def is_pos_possible(self, position_tested: Position) -> bool:
        return position_tested.compute_manhattan_dist(self.sensor_pos) > self._manhattan_dist

    @staticmethod
    def from_sensor_and_beacon_pos(sensor_pos: Position, closest_beacon_pos: Position) -> 'Sensor':
        to_ret = Sensor()

        to_ret.sensor_pos = sensor_pos
        to_ret.closest_beacon_pos = closest_beacon_pos
        to_ret._manhattan_dist = to_ret.sensor_pos.compute_manhattan_dist(to_ret.closest_beacon_pos)

        return to_ret


def parse_line(str_param: str) -> Sensor:
    matched_elem = re.findall(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", str_param)

    sensor_pos_x = int(matched_elem[0][0])
    sensor_pos_y = int(matched_elem[0][1])
    beacon_pos_x = int(matched_elem[0][2])
    beacon_pos_y = int(matched_elem[0][3])

    return Sensor.from_sensor_and_beacon_pos(Position(sensor_pos_x, sensor_pos_y), Position(beacon_pos_x, beacon_pos_y))


def compute_nb_unique_elem_in_list_range(list_range: List[range]) -> int:
    acc = 0

    list_already_accounted_for_range: List[range] = []
    list_already_substracted_range: List[range] = []
    for range_elem in list_range:
        list_range_added: List[range] = []
        list_range_substracted: List[range] = []
        acc += len(range_elem)

        for already_substracted_range in list_already_substracted_range:
            range_to_readd = range_overlap(range_elem, already_substracted_range)
            if range_to_readd is not None:
                list_range_added.append(range_to_readd)
                acc += len(range_to_readd)

        for already_counted_range in list_already_accounted_for_range:
            range_to_substract = range_overlap(range_elem, already_counted_range)
            if range_to_substract is not None:
                list_range_substracted.append(range_to_substract)
                acc -= len(range_to_substract)

        list_already_accounted_for_range.append(range_elem)
        list_already_accounted_for_range.extend(list_range_added)
        list_already_substracted_range.extend(list_range_substracted)

        if acc == 4000001:
            return acc

    return acc


def main():
    with open("data.txt") as f:
        content = [parse_line(line) for line in f.read().splitlines()]

    dict_nb_beacon_pos_per_line: Dict[int, int] = collections.defaultdict(lambda: 0)

    for sensor in content:
        beacon_y_pos = sensor.closest_beacon_pos.y
        beacon_x_pos = sensor.closest_beacon_pos.x

        if min_pos <= beacon_y_pos <= max_pos and min_pos <= beacon_x_pos <= max_pos:
            dict_nb_beacon_pos_per_line[sensor.closest_beacon_pos.y] += 1

    y_beacon_pos: Optional[int] = None
    for y in range(max_pos):
        nb_pos_without_beacon_on_line = compute_nb_forbidden_pos_on_line(content, y)
        if y in dict_nb_beacon_pos_per_line:
            nb_pos_without_beacon_on_line += dict_nb_beacon_pos_per_line[y]
            print("problem avoided", y)
        if nb_pos_without_beacon_on_line == max_pos:
            y_beacon_pos = y
            break

    if y_beacon_pos is None:
        raise AssertionError("expected to have an y by now")
    else:
        print("found y", y_beacon_pos)

    for x in range(4000001):
        candidate_pos = Position(x, y_beacon_pos)
        is_pos_valid: bool = True
        for beacon in content:
            if not beacon.is_pos_possible(candidate_pos):
                is_pos_valid = False
                break
        if is_pos_valid:
            print(candidate_pos)
            break

    # print(list_range_pos_without_beacon_on_line)
    # 3149438 too low
    # 5180742 too high
    # print(nb_pos_without_beacon_on_line)


def compute_nb_forbidden_pos_on_line(content, line_number: int) -> int:
    list_range_pos_without_beacon_on_line: List[range] = []
    for sensor in content:
        # candidate_range = sensor.get_range_pos_without_beacon_on_line(10)
        candidate_range = sensor.get_range_pos_without_beacon_on_line(line_number)
        if candidate_range is not None:
            list_range_pos_without_beacon_on_line.append(candidate_range)
    nb_pos_without_beacon_on_line = compute_nb_unique_elem_in_list_range(list_range_pos_without_beacon_on_line)
    return nb_pos_without_beacon_on_line


if __name__ == "__main__":
    main()
