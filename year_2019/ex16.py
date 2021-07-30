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

# input_str = "03036732577212944063491565474664"
# input_str = "02935109699940807407585447034323"


@lru_cache(maxsize=None)
def get_mult_pattern_for_num(num: int, max_len: int) -> [float]:
    pattern_array: [float] = []
    for _ in range(num + 1):
        pattern_array.append(0)
    for _ in range(num + 1):
        pattern_array.append(1)
    for _ in range(num + 1):
        pattern_array.append(0)
    for _ in range(num + 1):
        pattern_array.append(-1)

    long_enough_pattern = pattern_array * (int(max_len / 4) + 1)
    return long_enough_pattern[1:]


def apply_one_phase_on_num(num_to_transform: str) -> str:
    digit_list = [int(digit) for digit in num_to_transform]
    size_num = len(digit_list)

    num_to_ret = ""
    for num_rank in range(size_num):
        mult_pattern = get_mult_pattern_for_num(num_rank, size_num)
        acc = 0

        inner_rank = 0
        # N ^2 complexity, will probably take forever :grimacing:
        for num in digit_list:
            acc += num * mult_pattern[inner_rank]
            inner_rank += 1
        num_to_ret += str(acc)[-1]
    return num_to_ret


def apply_one_truncated_phase_on_num(num_to_transform: str) -> str:
    digit_list = [int(digit) for digit in num_to_transform]
    size_num = len(digit_list)
    acc = ""
    sum_digits = sum(digit_list)
    for num_rank in range(0, size_num):
        acc += str(sum_digits)[-1]
        sum_digits -= digit_list[num_rank]

    return acc


next_phase_input = input_str * 10000

offset = int(next_phase_input[:7])


# given the offset is SO close to the number total size (the total size is MUCH below twice the offset, and only
# SLIGHTLY bigger than the offset), we can take into account only the end of the number and consider every number to be
# ones up to the end

truncated_next_phase_input = next_phase_input[offset:]
print(len(truncated_next_phase_input))
for _ in range(100):
    print(f"phase {_} done")

    truncated_next_phase_input = apply_one_truncated_phase_on_num(truncated_next_phase_input)

# 13877442 too high
print(truncated_next_phase_input[:8])
