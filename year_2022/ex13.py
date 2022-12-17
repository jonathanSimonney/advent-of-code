from typing import List, Union, Optional


class IntValue:
    data: int

    def __lt__(self, other):
        if isinstance(other, IntValue):
            pass
        elif isinstance(other, ListValue):
            pass
        raise AssertionError("expected a value param")

    # def __gt__(self, other):
    #     if isinstance(other, IntValue):
    #         pass
    #     elif isinstance(other, ListValue):
    #         pass
    #     raise AssertionError("expected a value param")
    #
    # def __eq__(self, other):
    #     if isinstance(other, IntValue):
    #         pass
    #     elif isinstance(other, ListValue):
    #         pass
    #     raise AssertionError("expected a value param")

    @staticmethod
    def from_str(init_str) -> 'IntValue':
        pass


class ListValue:
    data: List[Union[IntValue, 'ListValue']]

    def __lt__(self, other):
        if isinstance(other, IntValue):
            pass
        elif isinstance(other, ListValue):
            pass
        raise AssertionError("expected a value param")

    # def __gt__(self, other):
    #     if isinstance(other, IntValue):
    #         pass
    #     elif isinstance(other, ListValue):
    #         pass
    #     raise AssertionError("expected a value param")
    #
    # def __eq__(self, other):
    #     if isinstance(other, IntValue):
    #         pass
    #     elif isinstance(other, ListValue):
    #         pass
    #     raise AssertionError("expected a value param")

    @staticmethod
    def from_str(init_str) -> 'ListValue':
        pass


class Packet:
    list_elems: ListValue

    def __lt__(self, other):
        if isinstance(other, Packet):
            pass
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
        pass


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

    acc: int = 0
    for pair in pair_list:
        if pair[0] < pair[1]:
            acc += 1


if __name__ == "__main__":
    main()
