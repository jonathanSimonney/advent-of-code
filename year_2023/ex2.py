from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class ColorDices(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


dict_color_to_nb_dices: Dict[ColorDices, int] = {
    ColorDices.RED: 12,
    ColorDices.GREEN: 13,
    ColorDices.BLUE: 14
}

dict_str_color_to_enum: Dict[str, ColorDices] = {
    'red': ColorDices.RED,
    'green': ColorDices.GREEN,
    'blue': ColorDices.BLUE
}


class Game:
    id_game: int
    _reveals_list: List[dict[ColorDices, int]]

    def __init__(self, id_game: int, reveals_list: List[dict[ColorDices, int]]):
        self.id_game = id_game
        self._reveals_list = reveals_list

    def is_game_possible(self) -> bool:
        for reveal in self._reveals_list:
            for color, nb_dices in reveal.items():
                if nb_dices > dict_color_to_nb_dices[color]:
                    return False
        return True

    def compute_game_power(self) -> int:
        min_set_cubes = self._compute_min_set_cube_needed()

        power = 1

        for num_cubes in min_set_cubes.values():
            power *= num_cubes

        return power

    def _compute_min_set_cube_needed(self) -> dict[ColorDices, int]:
        dict_color_to_min_nb_dices: Dict[ColorDices, int] = {
            ColorDices.RED: 0,
            ColorDices.GREEN: 0,
            ColorDices.BLUE: 0
        }

        for reveal in self._reveals_list:
            for color, nb_dices in reveal.items():
                if nb_dices > dict_color_to_min_nb_dices[color]:
                    dict_color_to_min_nb_dices[color] = nb_dices

        return dict_color_to_min_nb_dices



def parse_reveal_str_as_dict(reveal_str: str) -> dict[ColorDices, int]:
    reveal_dict: dict[ColorDices, int] = {}

    reveal_array = reveal_str.split(", ")
    for single_dice_reveal in reveal_array:
        single_dice_reveal_array = single_dice_reveal.split(" ")

        dice_int = int(single_dice_reveal_array[0])
        dice_color = dict_str_color_to_enum[single_dice_reveal_array[1]]

        reveal_dict[dice_color] = dice_int

    return reveal_dict


def parse_line_content_as_game(line_to_parse: str) -> Game:

    line_to_parse_array = line_to_parse.split(": ")

    game_part = line_to_parse_array[0]
    reveals_part = line_to_parse_array[1]

    game_id = int(game_part.split(" ")[1])

    reveals_str_array = reveals_part.split("; ")
    reveals_list: List[dict[ColorDices, int]] = []

    for reveal_str in reveals_str_array:
        reveals_list.append(parse_reveal_str_as_dict(reveal_str))

    return Game(game_id, reveals_list)


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [parse_line_content_as_game(x.strip()) for x in content]

acc = 0

for game in content:
    # if game.is_game_possible():
    acc += game.compute_game_power()

# 53706 too low
print(acc)
