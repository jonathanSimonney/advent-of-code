from dataclasses import dataclass
from typing import Set, List, Dict

from common_helpers.position import Direction, Position


def main():
    with open("data.txt") as f:
        content = f.read().splitlines()

    dict_add_instructions: Dict[int, int] = {}

    nb_cycle = 0

    for nb_line, line in enumerate(content):
        if line != 'noop':
            nb_cycle += 2
            dict_add_instructions[nb_cycle] = int(line.split(' ')[1])
        else:
            nb_cycle += 1

    acc = 0
    registry_value = 1
    for nb_cycle in range(nb_cycle):
        if nb_cycle in [20, 60, 100, 140, 180, 220]:
            acc += nb_cycle * registry_value
        if nb_cycle in dict_add_instructions:
            registry_value += dict_add_instructions[nb_cycle]

    print(acc)

if __name__ == "__main__":
    main()
