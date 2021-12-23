from typing import TypedDict

from common_helpers.position import Position


class ImageWorldDict(TypedDict):
    dict_known_image: dict[Position, str]
    char_outside_world: str
    min_y: int
    min_x: int
    max_y: int
    max_x: int


def parse_bin_str_to_int(str_to_parse: str) -> int:
    return int(str_to_parse, 2)


def get_char_in_image(image: ImageWorldDict, position_char: Position) -> str:
    try:
        return image['dict_known_image'][position_char]
    except KeyError:
        return image['char_outside_world']


def compute_new_image_pixel(
        image_to_enhance: ImageWorldDict,
        x_coord: int,
        y_coord: int,
        algorithm_enhancement: str
) -> str:
    str_binary = ''
    for x in range(x_coord - 1, x_coord + 2):
        for y in range(y_coord - 1, y_coord + 2):
            if get_char_in_image(image_to_enhance, Position(x, y)) == '#':
                str_binary += '1'
            else:
                str_binary += '0'

    return algorithm_enhancement[parse_bin_str_to_int(str_binary)]


def apply_image_enhancement_algorithm(image_to_enhance: ImageWorldDict, algorithm_enhancement: str):
    image_to_enhance['min_x'] -= 2
    image_to_enhance['min_y'] -= 2
    image_to_enhance['max_x'] += 2
    image_to_enhance['max_y'] += 2

    new_dict_known_image: dict[Position, str] = {}
    for x in range(image_to_enhance['min_x'], image_to_enhance['max_x']):
        for y in range(image_to_enhance['min_y'], image_to_enhance['max_y']):
            new_dict_known_image[Position(x, y)] = compute_new_image_pixel(
                image_to_enhance,
                x,
                y,
                algorithm_enhancement
            )

    image_to_enhance['dict_known_image'] = new_dict_known_image
    image_to_enhance['char_outside_world'] = algorithm_enhancement[-1] \
        if image_to_enhance['char_outside_world'] == "#" else algorithm_enhancement[0]


def main():
    with open("data.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [line.strip() for line in content]

    image_enhancement_algorithm: str = content[0]

    dict_known_image: dict[Position, str] = {}

    min_y = 0
    min_x = 0
    max_x = len(content[2:])
    max_y = len(content[2:][0])

    for x, line in enumerate(content[2:]):
        for y, char in enumerate(line):
            dict_known_image[Position(x, y)] = char

    image_to_enhance: ImageWorldDict = {
        'dict_known_image': dict_known_image,
        'char_outside_world': '.',
        'min_y': min_y,
        'min_x': min_x,
        'max_y': max_y,
        'max_x': max_x
    }

    for _ in range(50):
        apply_image_enhancement_algorithm(image_to_enhance, image_enhancement_algorithm)
        print("another enhancement was done")

    nb_lit_pixels = 0
    for char in image_to_enhance['dict_known_image'].values():
        if char == '#':
            nb_lit_pixels += 1

    print(nb_lit_pixels)


if __name__ == "__main__":
    main()
