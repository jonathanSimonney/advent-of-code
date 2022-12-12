from dataclasses import dataclass
from typing import Set, List, Dict

from common_helpers.position import Direction, Position


def main():
    with open("data.txt") as f:
        content = f.read().splitlines()

    dict_add_instructions: Dict[int, int] = {}

    nb_cycle = 1

    for nb_line, line in enumerate(content):
        if line != 'noop':
            nb_cycle += 2
            dict_add_instructions[nb_cycle] = int(line.split(' ')[1])
        else:
            nb_cycle += 1

    acc = 0
    registry_value = 1
    acc_str = ''
    for nb_cycle in range(1, nb_cycle + 1):
        if nb_cycle in dict_add_instructions:
            registry_value += dict_add_instructions[nb_cycle]
        if registry_value - 1 <= nb_cycle % 40 - 1 <= registry_value + 1:
            acc_str += '#'
        else:
            acc_str += '.'
        if nb_cycle in [20, 60, 100, 140, 180, 220]:
            acc += nb_cycle * registry_value

    print(acc)
    print(acc_str[:40])
    print(acc_str[40:80])
    print(acc_str[80:120])
    print(acc_str[120:160])
    print(acc_str[160:200])
    print(acc_str[200:240])


if __name__ == "__main__":
    main()
