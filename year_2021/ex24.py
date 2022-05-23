from dataclasses import dataclass
from enum import Enum, auto
from typing import Union, Callable, TypedDict


class SimplifiedParam(TypedDict):
    z_divisor: int
    x_add: int
    z_eventual_add: int


@dataclass(frozen=True)
class ZPossibleNum:
    min_remainder: int
    max_remainder: int
    nb_26_multiplicateurs_applied: int
    parent_z: Union['ZPossibleNum', None]
    # child_z_1: Union['ZPossibleNum', None]
    # child_z_2: Union['ZPossibleNum', None]


class DataForIdxGuess(TypedDict):
    z_possibilities: list[ZPossibleNum]

# list params more easy :
list_params: list[SimplifiedParam] = [
    {
        "z_divisor": 1,
        "x_add": 11,
        "z_eventual_add": 8
    },
    {
        "z_divisor": 1,
        "x_add": 14,
        "z_eventual_add": 13
    },
    {
        "z_divisor": 1,
        "x_add": 10,
        "z_eventual_add": 2
    },
    {
        "z_divisor": 26,
        "x_add": 0,
        "z_eventual_add": 7
    },
    {
        "z_divisor": 1,
        "x_add": 12,
        "z_eventual_add": 11
    },
    {
        "z_divisor": 1,
        "x_add": 12,
        "z_eventual_add": 4
    },
    {
        "z_divisor": 1,
        "x_add": 12,
        "z_eventual_add": 13
    },
    {
        "z_divisor": 26,
        "x_add": -8,
        "z_eventual_add": 13
    },
    {
        "z_divisor": 26,
        "x_add": -9,
        "z_eventual_add": 10
    },
    {
        "z_divisor": 1,
        "x_add": 11,
        "z_eventual_add": 1
    },
    {
        "z_divisor": 26,
        "x_add": 0,
        "z_eventual_add": 2
    },
    {
        "z_divisor": 26,
        "x_add": -5,
        "z_eventual_add": 14
    },
    {# 1 : z = [7,15]
        #2 : z = [26*13, 26*21] + [7, 15]
        "z_divisor": 26,
        "x_add": -6,
        "z_eventual_add": 6
    },# 1 : z was = 0, input_user = [7, 9]
    # 2 : z was != 0 (ergo, z = [26*13, 26*22], input_user = self.x_var,
    { # z = [13, 22]
        "z_divisor": 26,
        "x_add": -12,
        "z_eventual_add": 14
    } # z = 0, #x = [1, 9]
    # z = 26 * z' + R (with R = [1, 25])
]

bottom_z: ZPossibleNum = ZPossibleNum(13, 21, 0, None)


def generate_z_children(parent_z: ZPossibleNum, instruction_ending_with_parent: SimplifiedParam) -> list[ZPossibleNum]:
    pass


def main():
    dict_number_to_guess: dict[int, DataForIdxGuess] = {}
    dict_number_to_guess[13] = {'z_possibilities': [bottom_z]}
    for i in range(12, -1, -1):
        list_to_fill: list[ZPossibleNum] = []

        for possible_num in dict_number_to_guess[i + 1]['z_possibilities']:
            list_to_fill.extend(generate_z_children(possible_num, list_params[i]))

        dict_number_to_guess[i] = {'z_possibilities': list_to_fill}

    num_to_display = ''

    list_origin_path = []
    for possibility in dict_number_to_guess[0]['z_possibilities']:
        if possibility.min_remainder == 0 and possibility.nb_26_multiplicateurs_applied == 0:
            list_origin_path.append(possibility)
    print(list_origin_path)


if __name__ == "__main__":
    main()

# tactique : remonter la liste de Z en partant du bas, ça fera 2**14 possibilité, nettement moins que les 9**14
# possibilités pour la structure d'un z, besoin : le parent, les 2 enfants, le nb de multiplicateurs 26 qu'on a qui
# traînent, et le reste (derrière tt les multiplicateurs de 26 quoi)

# MONAD current state :
# W inp_2
# X 0
# Y inp_1 + 8
# Z 0
