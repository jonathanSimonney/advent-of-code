import math
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
    # first, we EXPLODE
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
                snailfish_num_as_list = snailfish_num_to_explode.split(',')
                snailfish_num_left = int(snailfish_num_as_list[0])
                snailfish_num_right = int(snailfish_num_as_list[1])

                new_str = add_num_to_leftmost(str_list_already_seen, snailfish_num_left) + '0' + add_num_to_rightmost(str_list_not_yet_seen, snailfish_num_right)
                return reduce_snailfish_str(new_str)
        else:
            if must_explode_next_snailfish_num:
                snailfish_num_to_explode += char

    # then, we SPLIT
    str_list_not_yet_seen = list(str_to_reduce)
    str_list_already_seen = []
    str_num = ''
    for char in str_to_reduce:
        str_list_already_seen.append(char)
        if char in ['[', ']', ',']:
            if str_num != '':
                str_list_already_seen.pop()
                if int(str_num) >= 10:
                    halved_num = int(str_num) / 2
                    replacement_snailfish_num = f"[{str(math.floor(halved_num))},{str(math.ceil(halved_num))}]"

                    new_str = ''.join(str_list_already_seen) + replacement_snailfish_num + ''.join(str_list_not_yet_seen)

                    return reduce_snailfish_str(new_str)

                str_list_already_seen.append(str_num)
                str_list_already_seen.append(char)
                str_num = ''
        else:
            str_num += char
            str_list_already_seen.pop()
        str_list_not_yet_seen.pop(0)

    return str_to_reduce


def add_two_snailfish_numbers(nb_1: str, nb_2: str) -> str:
    return reduce_snailfish_str(f"[{nb_1},{nb_2}]")


def compute_snailfish_num_magnitude(snailfish_num: str) -> int:
    if '[' not in snailfish_num:
        return int(snailfish_num)

    snailfish_num_1 = ''
    snailfish_num_2 = ''
    nb_opened_brackets = 0
    have_filled_all_num_1 = False

    for char in snailfish_num[1:-1]:
        if have_filled_all_num_1:
            snailfish_num_2 += char
        else:
            snailfish_num_1 += char
        if char == '[':
            nb_opened_brackets += 1
        elif char == ']':
            nb_opened_brackets -= 1
        elif char == ',' and nb_opened_brackets == 0:
            snailfish_num_1 = ''.join(list(snailfish_num_1)[:-1])
            have_filled_all_num_1 = True

    return 3*compute_snailfish_num_magnitude(snailfish_num_1) + 2*compute_snailfish_num_magnitude(snailfish_num_2)


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [line.strip() for line in content]

snailfish_sum = content[0]
# print(snailfish_sum)
for line in content[1:]:
    snailfish_sum = add_two_snailfish_numbers(snailfish_sum, line)
    # print(snailfish_sum)

print(snailfish_sum)
print(compute_snailfish_num_magnitude(snailfish_sum))
