import collections
from dataclasses import dataclass
from typing import Set, List, Dict, Callable, TypedDict

from common_helpers.position import Direction, Position


class MonkeyData:
    list_items: List[int]
    operation: str
    test_divider: int
    test_ok_target: int
    test_not_ok_target: int


class Monkey:
    items_worry_level: List[int]
    operation_performed: Callable[[int], int]
    get_number_targeted_monkey: Callable[[int], int]
    nb_time_inspected_items: int

    def __init__(
            self,
            items_worry_level: List[int],
            operation_performed: Callable[[int], int],
            get_number_targeted_monkey: Callable[[int], int]
    ):
        self.items_worry_level = items_worry_level
        self.operation_performed = operation_performed
        self.get_number_targeted_monkey = get_number_targeted_monkey
        self.nb_time_inspected_items = 0

    def take_turn(self) -> Dict[int, List[int]]:
        dict_to_ret: Dict[int, List[int]] = collections.defaultdict(lambda: list())
        for worry_level in self.items_worry_level:
            new_worry_level = self.operation_performed(worry_level)
            dict_to_ret[self.get_number_targeted_monkey(new_worry_level)].append(new_worry_level)
            self.nb_time_inspected_items += 1
        self.items_worry_level = []
        return dict_to_ret

    def receive_items(self, items_received: List[int]):
        self.items_worry_level.extend(items_received)


def play_round(list_monkeys: List[Monkey]):
    for monkey in list_monkeys:
        dict_thrown_items = monkey.take_turn()
        for monkey_num, list_thrown_items in dict_thrown_items.items():
            list_monkeys[monkey_num].receive_items(list_thrown_items)


def parse_operation(operation: str) -> Callable[[int], int]:
    if operation == 'old * old':
        return lambda worry_level: worry_level * worry_level
    splitted_operation = operation.split(' ')
    if splitted_operation[1] == '+':
        return lambda worry_level: worry_level + int(splitted_operation[2])
    elif splitted_operation[1] == '*':
        return lambda worry_level: worry_level * int(splitted_operation[2])
    raise AttributeError('couldn\'t parse operation ' + operation)


def build_monkey_from_dataclass(monkey_data: MonkeyData) -> Monkey:
    def get_number_targeted_monkey(worry_level: int) -> int:
        if worry_level % monkey_data.test_divider == 0:
            return monkey_data.test_ok_target
        return monkey_data.test_not_ok_target

    monkey_to_add = Monkey(
        monkey_data.list_items,
        parse_operation(monkey_data.operation),
        get_number_targeted_monkey
    )
    return monkey_to_add


def main():
    with open("data.txt") as f:
        content = f.read().splitlines()

    list_monkeys: List[Monkey] = []

    monkey_data: MonkeyData = MonkeyData()
    for line in content:
        if line == '':
            monkey_to_add = build_monkey_from_dataclass(monkey_data)
            list_monkeys.append(monkey_to_add)
            monkey_data = MonkeyData()
        else:
            splitted_line = line.strip().split(':')
            if splitted_line[0] == 'Starting items':
                monkey_data.list_items = [int(x) for x in splitted_line[1].split(', ')]
            elif splitted_line[0] == 'Operation':
                monkey_data.operation = splitted_line[1].split(' = ')[1]
            elif splitted_line[0] == 'Test':
                monkey_data.test_divider = int(splitted_line[1].split(' ')[-1])
            elif splitted_line[0] == 'If true':
                monkey_data.test_ok_target = int(splitted_line[1].split(' ')[-1])
            elif splitted_line[0] == 'If false':
                monkey_data.test_not_ok_target = int(splitted_line[1].split(' ')[-1])

    monkey_to_add = build_monkey_from_dataclass(monkey_data)
    list_monkeys.append(monkey_to_add)

    for _ in range(10000):
        play_round(list_monkeys)

    ordered_list_monkeys_nb_time_inspected_items = sorted([monkey.nb_time_inspected_items for monkey in list_monkeys])
    # 23220 too low
    print(ordered_list_monkeys_nb_time_inspected_items)
    print(ordered_list_monkeys_nb_time_inspected_items[-1] * ordered_list_monkeys_nb_time_inspected_items[-2])


if __name__ == "__main__":
    main()
