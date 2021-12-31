from typing import TypedDict

from common_helpers.position import Cuboid, compute_intersection_cuboid


class CuboidDict(TypedDict):
    cuboid: Cuboid
    is_on: bool


def parse_input_range(range_as_str: str) -> [int]:
    list_range = range_as_str.split('..')
    return [int(range_str) for range_str in list_range]


def parse_line(input_line: str) -> CuboidDict:
    line_splitted = input_line.split(" ")
    is_on: bool = line_splitted[0] == 'on'

    splitted_coordinates = line_splitted[1].split(',')

    x_range = parse_input_range(splitted_coordinates[0][2:])
    y_range = parse_input_range(splitted_coordinates[1][2:])
    z_range = parse_input_range(splitted_coordinates[2][2:])

    cuboid: Cuboid = Cuboid(
        x_range[0],
        x_range[1],
        y_range[0],
        y_range[1],
        z_range[0],
        z_range[1]
    )

    return {'is_on': is_on, 'cuboid': cuboid}


def compute_total_nb_cubes_on(list_on_cuboids: list[Cuboid], list_off_cuboids: list[Cuboid]) -> int:
    acc = 0
    for cuboid in list_on_cuboids:
        acc += cuboid.compute_volume()

    for cuboid in list_off_cuboids:
        acc -= cuboid.compute_volume()

    return acc


def main():
    with open("data.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [parse_line(line.strip()) for line in content]

    list_on_cubes: list[Cuboid] = []
    list_off_cubes: list[Cuboid] = []

    print(content)
    for cuboid_dict in content:
        # if not -50 <= cuboid_dict['cuboid'].x_min <= 50:
        #     break

        to_append_to_list_on: list[Cuboid] = []
        to_append_to_list_off: list[Cuboid] = []

        for cuboid_on in list_on_cubes:
            intersect_cuboid = compute_intersection_cuboid(cuboid_dict['cuboid'], cuboid_on)
            if intersect_cuboid is not None:
                to_append_to_list_off.append(intersect_cuboid)
        for cuboid_off in list_off_cubes:
            intersect_cuboid = compute_intersection_cuboid(cuboid_dict['cuboid'], cuboid_off)
            if intersect_cuboid is not None:
                to_append_to_list_on.append(intersect_cuboid)

        list_on_cubes.extend(to_append_to_list_on)
        list_off_cubes.extend(to_append_to_list_off)
        if cuboid_dict['is_on']:
            list_on_cubes.append(cuboid_dict['cuboid'])

    # 614106 too low
    print(compute_total_nb_cubes_on(list_on_cubes, list_off_cubes))


if __name__ == "__main__":
    main()
