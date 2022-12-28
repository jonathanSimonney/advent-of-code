import re
from typing import List, Optional

from common_helpers.position import Position
from common_helpers.range_helper import range_overlap, create_inclusive_range_properly_ordered


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
        return range(x_range_lower, x_range_upper + 1)

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

    return acc


def main():
    with open("data.txt") as f:
        content = [parse_line(line) for line in f.read().splitlines()]

    list_range_pos_without_beacon_on_line: List[range] = []
    for sensor in content:
        # candidate_range = sensor.get_range_pos_without_beacon_on_line(10)
        candidate_range = sensor.get_range_pos_without_beacon_on_line(2000000)
        if candidate_range is not None:
            list_range_pos_without_beacon_on_line.append(candidate_range)

    print(list_range_pos_without_beacon_on_line)
    # 3149438 too low
    # 5180742 too high
    print(compute_nb_unique_elem_in_list_range(list_range_pos_without_beacon_on_line))


if __name__ == "__main__":
    main()
