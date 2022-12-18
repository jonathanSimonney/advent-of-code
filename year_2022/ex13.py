from typing import List, Union, Optional
import sys
sys.setrecursionlimit(5000)


class IntValue:
    data: int

    def __lt__(self, other):
        if isinstance(other, IntValue):
            return self.data < other.data
        elif isinstance(other, ListValue):
            return compare_list_values(ListValue.from_str(f'[{self.data}]'), other) == -1
        raise AssertionError("expected a value param")

    def __gt__(self, other):
        if isinstance(other, IntValue):
            return self.data > other.data
        elif isinstance(other, ListValue):
            return compare_list_values(ListValue.from_str(f'[{self.data}]'), other) == 1
        raise AssertionError("expected a value param")
    #
    # def __eq__(self, other):
    #     if isinstance(other, IntValue):
    #         pass
    #     elif isinstance(other, ListValue):
    #         pass
    #     raise AssertionError("expected a value param")

    @staticmethod
    def from_str(init_str) -> 'IntValue':
        to_ret = IntValue()
        to_ret.data = int(init_str)
        return to_ret


# return 1 if list_value_1 > list_value_2,
# 0 if list_value_1 == list_value_2,
# and -1 if list_value_1 < list_value_2
def compare_list_values(list_value_1: 'ListValue', list_value_2: 'ListValue') -> int:
    for i in range(len(list_value_1.data)):
        data_1 = list_value_1.data[i]
        try:
            data_2 = list_value_2.data[i]
        except IndexError:
            return 1  # list 1 is longer than the other, so list 1 is the "greater" list
        if data_1 < data_2:
            return -1
        elif data_1 > data_2:
            return 1
    if len(list_value_2.data) > len(list_value_1.data):
        return -1  # list 1 ran out of elem before list 2
    return 0


class ListValue:
    data: List[Union[IntValue, 'ListValue']]

    def __lt__(self, other):
        if isinstance(other, IntValue):
            return compare_list_values(self, ListValue.from_str(f'[{other.data}]')) == -1
        elif isinstance(other, ListValue):
            return compare_list_values(self, other) == -1

        raise AssertionError("expected a value param")

    def __gt__(self, other):
        if isinstance(other, IntValue):
            return compare_list_values(self, ListValue.from_str(f'[{other.data}]')) == 1
        elif isinstance(other, ListValue):
            return compare_list_values(self, other) == 1
        raise AssertionError("expected a value param")
    #
    # def __eq__(self, other):
    #     if isinstance(other, IntValue):
    #         pass
    #     elif isinstance(other, ListValue):
    #         pass
    #     raise AssertionError("expected a value param")

    @staticmethod
    def from_str(init_str) -> 'ListValue':
        stripped_init_str = init_str[1:-1]

        to_ret = ListValue()
        to_ret.data = []

        # problem : splitting on the , doesn't properly handles [2],[1,2,3] i.e
        nb_unclosed_brackets: int = 0
        acc_list_str = ''
        for elem in stripped_init_str.split(','):
            if nb_unclosed_brackets == 0 and elem.isdigit():
                to_ret.data.append(IntValue.from_str(elem))
            else:
                nb_unclosed_brackets += elem.count('[')
                nb_unclosed_brackets -= elem.count(']')
                acc_list_str += elem
                if nb_unclosed_brackets == 0 and acc_list_str != '':
                    to_ret.data.append(ListValue.from_str(acc_list_str))
                    acc_list_str = ''
                else:
                    acc_list_str += ','

        return to_ret


class Packet:
    list_elems: ListValue

    def __lt__(self, other):
        if isinstance(other, Packet):
            return self.list_elems < other.list_elems
        raise AssertionError("expected a packet param")

    # def __gt__(self, other):
    #     if isinstance(other, Packet):
    #         pass
    #     raise AssertionError("expected a packet param")
    #
    # def __eq__(self, other):
    #     if isinstance(other, Packet):
    #         pass
    #     raise AssertionError("expected a packet param")

    @staticmethod
    def from_str(init_str) -> 'Packet':
        to_ret = Packet()
        to_ret.list_elems = ListValue.from_str(init_str)
        return to_ret


def main():
    with open("data.txt") as f:
        content = f.read().splitlines()

    left_pair: Optional[Packet] = None
    right_pair: Optional[Packet] = None

    pair_list: List[List[Packet]] = []
    for line in content:
        if left_pair is None:
            left_pair = Packet.from_str(line)
        elif right_pair is None:
            right_pair = Packet.from_str(line)
        else:
            pair_list.append([left_pair, right_pair])
            left_pair = None
            right_pair = None

    if left_pair is not None and right_pair is not None:
        pair_list.append([left_pair, right_pair])

    acc: int = 0
    for idx_pair, pair in enumerate(pair_list):
        if pair[0] < pair[1]:
            acc += idx_pair + 1

    print(acc)


if __name__ == "__main__":
    main()
