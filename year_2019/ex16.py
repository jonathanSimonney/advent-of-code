import collections
from functools import lru_cache
from typing import TypedDict, List

input_str = "59702216318401831752516109671812909117759516365269440231257788008453756734827826476239905226493589" \
            "00696013245648887029086289370353575369150724412015613780286431733093810668897362412459437160817069" \
            "25698557784981055174390680223883235666240692027534377428019818834737297014261710772779200138248947" \
            "57938493999640593305172570727136129712787668811072014245905885251704882055908305407719142264325661" \
            "47782589861980277786896143964772340883395784381011145636746461123901773304271729359887156630402042" \
            "64847000713152572170118722404923954510288728566055764928646461182925008135457478680960465774845352" \
            "23887886476125746077660705155595199557168004672030769602168262"

# input_str = "12345678"


def compute_resulting_num_dict_digit(dict_digit: dict) -> str:
    acc = 0
    for digit, multiplier in dict_digit.items():
        acc += digit * multiplier
    print(f"acc: {acc}")
    return str(acc)[-1]


# @lru_cache(maxsize=None)
# def get_mult_pattern_for_num(num: int, max_len: int) -> [float]:
#     pattern_array: [float] = []
#     for _ in range(num + 1):
#         pattern_array.append(0)
#     for _ in range(num + 1):
#         pattern_array.append(1)
#     for _ in range(num + 1):
#         pattern_array.append(0)
#     for _ in range(num + 1):
#         pattern_array.append(-1)
#
#     long_enough_pattern = pattern_array * (int(max_len / 4) + 1)
#     return long_enough_pattern[1:]


class MultPattern(TypedDict):
    index_to_add: List[int]
    index_to_substract: List[int]


def compute_mult_pattern_for_num(index_num: int, size_num: int) -> MultPattern:
    dict_acc: MultPattern = {"index_to_add": [], "index_to_substract": []}
    pos = index_num
    is_addition = True
    while pos < size_num:
        next_step_pos = pos + index_num + 1
        if is_addition:
            for i in range(pos, min(next_step_pos, size_num)):
                dict_acc["index_to_add"].append(i)
        else:
            for i in range(pos, min(next_step_pos, size_num)):
                dict_acc["index_to_substract"].append(i)
        pos = next_step_pos + index_num + 1
        is_addition = not is_addition

    return dict_acc

# constraints needed : I must skip the 0, AND can't re iterate over the whole number to compute a new digit.
# the struct that would be good would look like :
# [{"index_to_add": [1, 5, ...], "index_to_substract": [3, 7, 11, ...]}, ...]
def apply_one_phase_on_num(num_to_transform: str) -> str:
    digit_list = [int(digit) for digit in num_to_transform]
    size_num = len(digit_list)

    # list_nums_resulting = [{"mult_pattern": get_mult_pattern_for_num(num, size_num), "acc": 0, "actual_num": num} for num in digit_list]

    # print("pattern ready")
    # for num_rank in range(size_num):
    #     for num_dict in list_nums_resulting:
    #         num_dict["acc"] += num_dict["mult_pattern"][num_rank] * num_dict["actual_num"]
    #     print(f" one number done, to the next, {num_rank}")
    #
    #     # dict_digit = collections.defaultdict(int)
    #     # is_addition = True
    #     #
    #     # # inner_rank can start as num_rank because we skip all the 0 in the pattern, and we must strip the fist elem of
    #     # # the pattern list
    #     # inner_rank = num_rank
    #     #
    #     # while inner_rank < size_num:
    #     #     next_step_inner_rank = inner_rank + num_rank + 1
    #     #     if is_addition:
    #     #         for digit in digit_list[inner_rank:next_step_inner_rank]:
    #     #             dict_digit[digit] += 1
    #     #     else:
    #     #         for digit in digit_list[inner_rank:next_step_inner_rank]:
    #     #             dict_digit[digit] -= 1
    #     #     inner_rank = next_step_inner_rank + num_rank + 1
    #     #     is_addition = not is_addition
    #     # num_to_ret += compute_resulting_num_dict_digit(dict_digit)
    #     # print(f"we got one number for the chain, it is {num_to_ret}")
    # return "".join([str(num["acc"]) for num in list_nums_resulting])


next_phase_input = input_str * 10000

print(len(next_phase_input))
size_num = len(next_phase_input)
list_mult_patterns = [compute_mult_pattern_for_num(i, size_num) for i in range(size_num)]
print("computed all the patterns for mult")
# for _ in range(100):
#     print(f"phase {_} done")
#     print(f"param: {next_phase_input}")
#     print(len(next_phase_input))
#
#     next_phase_input = apply_one_phase_on_num(next_phase_input)
    # print(next_phase_input)

# 09012683 too low
# 05350576 too low
# offset = int(next_phase_input[:7])
# print(next_phase_input[offset:offset + 8])
