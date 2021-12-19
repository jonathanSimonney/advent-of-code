from statistics import median
from typing import Union

# class SnailfishNum:
#     left_num: Union[int, 'SnailfishNum']
#     right_num: Union[int, 'SnailfishNum']
#     parent: 'SnailfishNum'
#     depth: int
#
#     def __init__(self, left_num, right_num, parent, depth):
#         self.left_num = left_num
#         self.right_num = right_num
#         self.parent = parent
#         self.depth = depth
#
#     def reduce_while_able(self):
#         change_occured = True
#
#         while change_occured:
#             self._explode_while_able()
#             change_occured = self._split_while_able()
#
#     def _explode_while_able(self) -> bool:
#         pass
#
#     def _split_while_able(self) -> bool:
#         pass
#
#     def add_snailfish_num(self, other: 'SnailfishNum'):
#         pass
#
#     def compute_magnitude(self):
#         pass
#
#     def _add_to_right_elem(self):


def add_num_to_leftmost(ordered_list: list[str], num_to_add: int) -> str:
    reversed_list = []
    first_number_found = False
    parsed_first_number_entirely = False
    first_num_str_list = []
    for char in reversed(ordered_list):
        if parsed_first_number_entirely:
            reversed_list.append(char)
        else:
            if char in ['[', ']', ',']:
                if first_number_found:
                    reversed_list.append(str(int(''.join(reversed(first_num_str_list))) + num_to_add))
                    parsed_first_number_entirely = True
                reversed_list.append(char)
            else:
                first_number_found = True
                first_num_str_list.append(char)

    return ''.join(reversed(reversed_list))


def add_num_to_rightmost(ordered_list: list[str], num_to_add: int) -> str:
    ordered_list_acc = []
    first_number_found = False
    parsed_first_number_entirely = False
    first_num_str_list = []
    for char in ordered_list:
        if parsed_first_number_entirely:
            ordered_list_acc.append(char)
        else:
            if char in ['[', ']', ',']:
                if first_number_found:
                    ordered_list_acc.append(str(int(''.join(first_num_str_list)) + num_to_add))
                    parsed_first_number_entirely = True
                ordered_list_acc.append(char)
            else:
                first_number_found = True
                first_num_str_list.append(char)

    return ''.join(ordered_list_acc)


def reduce_snailfish_str(str_to_reduce: str) -> str:
    str_list_not_yet_seen = list(str_to_reduce)
    str_list_already_seen = []
    must_explode_next_snailfish_num = False
    snailfish_num_to_explode = ''
    nb_opened_brackets = 0
    for char in str_to_reduce:
        if not must_explode_next_snailfish_num:
            str_list_already_seen.append(char)
        str_list_not_yet_seen.pop(0)
        if char == '[':
            nb_opened_brackets += 1
            if nb_opened_brackets == 5:
                must_explode_next_snailfish_num = True
                str_list_already_seen.pop()
        elif char == ']':
            nb_opened_brackets -= 1
            if must_explode_next_snailfish_num:
                must_explode_next_snailfish_num = False
                snailfish_num_as_list = snailfish_num_to_explode.split(',')
                snailfish_num_left = int(snailfish_num_as_list[0])
                snailfish_num_right = int(snailfish_num_as_list[1])

                new_str = add_num_to_leftmost(str_list_already_seen, snailfish_num_left) + '0' + add_num_to_rightmost(str_list_not_yet_seen, snailfish_num_right)
                return reduce_snailfish_str(new_str)
        else:
            if must_explode_next_snailfish_num:
                snailfish_num_to_explode += char

    return str_to_reduce



with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [line.strip() for line in content]

print(reduce_snailfish_str('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]'))
