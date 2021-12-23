import collections
from typing import TypedDict, Union

from common_helpers.position import ThreeDPosition, compute_manhattan_dist


class ScannerDict(TypedDict):
    pos: ThreeDPosition
    beacon_num: int
    list_beacons_pos_relative_to_0: list[ThreeDPosition]
    list_beacons_pos_relative_to_scanner_pos: list[ThreeDPosition]
    unrelated_scanner_num: set[int]


def generate_list_in_all_24_orientations(base_list_orientation_0: list[ThreeDPosition]) -> list[list[ThreeDPosition]]:
    set_ref_point = set()

    list_to_ret = []

    for x_rotate in range(4):
        def x_transformation_method(point_to_transform: ThreeDPosition) -> ThreeDPosition:
            new_point = point_to_transform
            for _ in range(x_rotate + 1):
                new_point = new_point.get_point_rotated_over_x_axis()
            return new_point
        for y_rotate in range(4):
            def y_transformation_method(point_to_transform: ThreeDPosition) -> ThreeDPosition:
                new_point = point_to_transform
                for _ in range(y_rotate + 1):
                    new_point = new_point.get_point_rotated_over_y_axis()
                return new_point
            for z_rotate in range(4):
                def z_transformation_method(point_to_transform: ThreeDPosition) -> ThreeDPosition:
                    new_point = point_to_transform
                    for _ in range(z_rotate + 1):
                        new_point = new_point.get_point_rotated_over_z_axis()
                    return new_point

                new_list_orientations = [
                    x_transformation_method(y_transformation_method(z_transformation_method(pos))) for pos in base_list_orientation_0
                ]

                if new_list_orientations[0] not in set_ref_point:
                    list_to_ret.append(new_list_orientations)
                    set_ref_point.add(new_list_orientations[0])
    return list_to_ret


def find_unknown_origin_if_exist(
        list_relative_to_0: list[ThreeDPosition],
        list_relative_to_unknown_origin: list[ThreeDPosition]
) -> Union[ThreeDPosition, None]:
    dict_possible_origin_score = collections.defaultdict(lambda: 0)

    for point_relative_to_0 in list_relative_to_0:
        for point_relative_to_unknown in list_relative_to_unknown_origin:
            # need to understand how the eventual origin is actually calculated
            eventual_origin = ThreeDPosition(
                point_relative_to_0.x - point_relative_to_unknown.x,
                point_relative_to_0.y - point_relative_to_unknown.y,
                point_relative_to_0.z - point_relative_to_unknown.z
            )

            dict_possible_origin_score[eventual_origin] += 1

            if dict_possible_origin_score[eventual_origin] == 12:
                return eventual_origin

    return None


def compute_first_scanner_with_intersection(
        list_scanner_dicts: list[ScannerDict],
        dict_beacons_with_all_possible_pos: dict[int, list[list[ThreeDPosition]]]
) -> ScannerDict:

    for scanner_dict in list_scanner_dicts:
        for scanner_num, list_possible_pos_for_beacon in dict_beacons_with_all_possible_pos.items():
            if scanner_num in scanner_dict['unrelated_scanner_num']:
                continue

            for single_list in list_possible_pos_for_beacon:
                pos_scanner_or_none = find_unknown_origin_if_exist(
                    scanner_dict['list_beacons_pos_relative_to_0'],
                    single_list
                )

                # print(pos_scanner_or_none)
                if pos_scanner_or_none is not None:
                    return {
                        'beacon_num': scanner_num,
                        'list_beacons_pos_relative_to_scanner_pos': single_list,
                        'pos': pos_scanner_or_none,
                        'list_beacons_pos_relative_to_0': [
                            ThreeDPosition(
                                position_relative_to_pos.x + pos_scanner_or_none.x,
                                position_relative_to_pos.y + pos_scanner_or_none.y,
                                position_relative_to_pos.z + pos_scanner_or_none.z
                            ) for position_relative_to_pos in single_list
                        ],
                        'unrelated_scanner_num': set()
                    }
            scanner_dict['unrelated_scanner_num'].add(scanner_num)


def main():
    with open("data.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [line.strip() for line in content]

    list_scanner_dicts: list[ScannerDict] = []
    list_scanner_raw_beacons_results_in_24_possibles_orientations: dict[int, list[list[ThreeDPosition]]] = {}
    base_list_beacons: list[ThreeDPosition] = []

    scanner_num = 0
    for line in content:
        if line == '':
            list_scanner_raw_beacons_results_in_24_possibles_orientations[scanner_num] = \
                generate_list_in_all_24_orientations(base_list_beacons)
            base_list_beacons = []
            scanner_num += 1
        elif 'scanner' not in line:
            pos_list = line.split(',')
            base_list_beacons.append(ThreeDPosition(int(pos_list[0]), int(pos_list[1]), int(pos_list[2])))

    # forgot the tiny 30th
    list_scanner_raw_beacons_results_in_24_possibles_orientations[scanner_num] = \
        generate_list_in_all_24_orientations(base_list_beacons)

    list_scanner_dicts.append({
        'pos': ThreeDPosition(0, 0, 0),
        'beacon_num': 0,
        'list_beacons_pos_relative_to_0': list_scanner_raw_beacons_results_in_24_possibles_orientations[0][0],
        'list_beacons_pos_relative_to_scanner_pos': list_scanner_raw_beacons_results_in_24_possibles_orientations[0][0],
        'unrelated_scanner_num': set()
    })

    del(list_scanner_raw_beacons_results_in_24_possibles_orientations[0])
    while len(list_scanner_raw_beacons_results_in_24_possibles_orientations) != 0:
        new_scanner_dict = compute_first_scanner_with_intersection(
            list_scanner_dicts,
            list_scanner_raw_beacons_results_in_24_possibles_orientations
        )

        list_scanner_dicts.append(new_scanner_dict)
        del(list_scanner_raw_beacons_results_in_24_possibles_orientations[new_scanner_dict['beacon_num']])

    set_points = set()
    for scanner in list_scanner_dicts:
        set_points.update(scanner['list_beacons_pos_relative_to_0'])

    print(len(set_points))
    print(set_points)
    largest_manhattan_distance = 0
    for scanner in list_scanner_dicts:
        for inner_scanner in list_scanner_dicts:
            candidate_manhattan_dist = compute_manhattan_dist(scanner['pos'], inner_scanner['pos'])
            if candidate_manhattan_dist > largest_manhattan_distance:
                largest_manhattan_distance = candidate_manhattan_dist

    print(largest_manhattan_distance)


if __name__ == "__main__":
    main()
