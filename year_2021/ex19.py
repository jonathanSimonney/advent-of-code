import collections
from typing import TypedDict, Callable, Union

from common_helpers.position import ThreeDPosition


class ScannerDict(TypedDict):
    pos: ThreeDPosition
    beacon_num: int
    list_beacons_pos_relative_to_0: list[ThreeDPosition]
    list_beacons_pos_relative_to_scanner_pos: list[ThreeDPosition]
    unrelated_scanner_num: set[int]


# XYZ
# -ZYX
# -XY-Z
# -XY Z


# x     y    z
# -x    y    -z
# y    -x    z
# -y    x   z
# z     y   -x
# -z    y   x

# *

# yz, z-y, -y-z, -zy
# y-z, z-y, -y-z, -zy
# yz, z-y, -y-z, -zy
# yz, z-y, -y-z, -zy
# yz, z-y, -y-z, -zy
# yz, z-y, -y-z, -zy

# 24 because 4 *3 * 2 probably
def generate_list_in_all_24_orientations(base_list_orientation_0: list[ThreeDPosition]) -> list[list[ThreeDPosition]]:
    set_ref_point = set()

    list_to_ret = []
    # transform_pos_minus_func: Callable[[ThreeDPosition], ThreeDPosition]
    # transform_pos_order_func: Callable[[ThreeDPosition], ThreeDPosition]
    # for minus_transformation in range(8):
    #     if minus_transformation == 0:
    #         transform_pos_minus_func = lambda param: param
    #     elif minus_transformation == 1:
    #         transform_pos_minus_func = lambda param: ThreeDPosition(-param.x, param.y, param.z)
    #     elif minus_transformation == 2:
    #         transform_pos_minus_func = lambda param: ThreeDPosition(param.x, -param.y, param.z)
    #     elif minus_transformation == 3:
    #         transform_pos_minus_func = lambda param: ThreeDPosition(param.x, param.y, -param.z)
    #     elif minus_transformation == 4:
    #         transform_pos_minus_func = lambda param: ThreeDPosition(-param.x, -param.y, param.z)
    #     elif minus_transformation == 5:
    #         transform_pos_minus_func = lambda param: ThreeDPosition(-param.x, -param.y, -param.z)
    #     elif minus_transformation == 6:
    #         transform_pos_minus_func = lambda param: ThreeDPosition(-param.x, param.y, -param.z)
    #     elif minus_transformation == 7:
    #         transform_pos_minus_func = lambda param: ThreeDPosition(-param.x, -param.y, -param.z)
    #    # todo the pos calculated here are NOT the right ones. This need to be corrected!
    #     else:
    #         raise Exception("unexpected case")
    #
    #     for order_transformation in range(6):
    #         if order_transformation == 0:
    #             transform_pos_order_func = lambda param: param
    #         elif order_transformation == 1:
    #             transform_pos_order_func = lambda param: ThreeDPosition(param.x, param.z, param.y)
    #         elif order_transformation == 2:
    #             transform_pos_order_func = lambda param: ThreeDPosition(param.y, param.x, param.z)
    #         elif order_transformation == 3:
    #             transform_pos_order_func = lambda param: ThreeDPosition(param.y, param.z, param.x)
    #         elif order_transformation == 4:
    #             transform_pos_order_func = lambda param: ThreeDPosition(param.z, param.x, param.y)
    #         elif order_transformation == 5:
    #             transform_pos_order_func = lambda param: ThreeDPosition(param.z, param.y, param.x)
    #         else:
    #             raise Exception("unexpected case")
    #
    #         new_list_orientations = [
    #             transform_pos_minus_func(transform_pos_order_func(pos)) for pos in base_list_orientation_0
    #         ]
    #
    #         if new_list_orientations[0] not in set_ref_point:
    #             list_to_ret.append(new_list_orientations)
    #             set_ref_point.add(new_list_orientations[0])
    #         # if order_transformation == 1:
    #         #     print(transform_pos_order_func(ThreeDPosition(1, 2, 3)))
    #
    #         # print(new_list_orientations[0])
    #         # print(list_to_ret)
    #         # print(len(list_to_ret))
    #
    # print(list_to_ret[0][0], list_to_ret[1][0])

    # for main_axis in range(6):
    #     if main_axis == 0:
    #         def compute_point_with_main_axis(original_point: ThreeDPosition) -> ThreeDPosition:
    #             return original_point
    #     elif main_axis == 1:
    #         def compute_point_with_main_axis(original_point: ThreeDPosition) -> ThreeDPosition:
    #             return ThreeDPosition(-original_point.x, original_point.y, original_point.z)
    #     elif main_axis == 2:
    #         def compute_point_with_main_axis(original_point: ThreeDPosition) -> ThreeDPosition:
    #             return ThreeDPosition(original_point.x, original_point.y, original_point.z)
    #     elif main_axis == 3:
    #         transform_pos_order_func = lambda param: ThreeDPosition(param.y, param.z, param.x)
    #     elif main_axis == 4:
    #         transform_pos_order_func = lambda param: ThreeDPosition(param.z, param.x, param.y)
    #     elif main_axis == 5:
    #         transform_pos_order_func = lambda param: ThreeDPosition(param.z, param.y, param.x)
    #     else:
    #         raise Exception("unexpected case")

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
    print(len(list_to_ret))
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
                # print("found one", eventual_origin)
                return eventual_origin

    # if ThreeDPosition(-618,-824,-621) in list_relative_to_0 and ThreeDPosition(-686,422,-578) in list_relative_to_unknown_origin:
    #     print(dict_possible_origin_score)
    #     print(dict_possible_origin_score[ThreeDPosition(68,-1246,-43)])
    # print(dict_possible_origin_score)
    return None

nb_scanner_found = 1

def compute_first_scanner_with_intersection(
        list_scanner_dicts: list[ScannerDict],
        dict_beacons_with_all_possible_pos: dict[int, list[list[ThreeDPosition]]]
) -> ScannerDict:
    global nb_scanner_found

    for scanner_dict in list_scanner_dicts:
        for scanner_num, list_possible_pos_for_beacon in dict_beacons_with_all_possible_pos.items():
            if scanner_num in scanner_dict['unrelated_scanner_num']:
                continue

            # print(list_possible_pos_for_beacon[0][0])
            # print(list_possible_pos_for_beacon[1][0])
            for single_list in list_possible_pos_for_beacon:
                # if ThreeDPosition(686,422,578) in single_list:
                #     print("one threed pos found")
                # elif ThreeDPosition(-686,422,-578) in single_list:
                #     print("other threed pos found")
                #     # raise Exception
                # print(single_list[0])
                pos_scanner_or_none = find_unknown_origin_if_exist(
                    scanner_dict['list_beacons_pos_relative_to_0'],
                    single_list
                )

                # print(pos_scanner_or_none)
                if pos_scanner_or_none is not None:
                    print("found scanner num", scanner_num)
                    nb_scanner_found += 1
                    print(nb_scanner_found, 30 - nb_scanner_found)
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

    print("too much debug", base_list_beacons[-1])
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
        print(new_scanner_dict)

        if new_scanner_dict is None:
            print("no match found between ", list_scanner_dicts, "and")
            print([key_val for key_val in list_scanner_raw_beacons_results_in_24_possibles_orientations.keys()],
                  [len(value) for value in list_scanner_raw_beacons_results_in_24_possibles_orientations.values()])
        list_scanner_dicts.append(new_scanner_dict)
        del(list_scanner_raw_beacons_results_in_24_possibles_orientations[new_scanner_dict['beacon_num']])

    set_points = set()
    for scanner in list_scanner_dicts:
        set_points.update(scanner['list_beacons_pos_relative_to_0'])

    print(len(set_points))
    print(set_points)


if __name__ == "__main__":
    main()
