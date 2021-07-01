import collections
from functools import lru_cache

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


def apply_one_phase_on_num(num_to_transform: str) -> str:
    digit_list = [int(digit) for digit in num_to_transform]
    size_num = len(digit_list)

    num_to_ret = ""
    for num_rank in range(size_num):
        dict_digit = collections.defaultdict(int)
        is_addition = True

        # inner_rank can start as num_rank because we skip all the 0 in the pattern, and we must strip the fist elem of
        # the pattern list
        inner_rank = num_rank

        while inner_rank < size_num:
            next_step_inner_rank = inner_rank + num_rank + 1
            if is_addition:
                for digit in digit_list[inner_rank:next_step_inner_rank]:
                    dict_digit[digit] += 1
            else:
                for digit in digit_list[inner_rank:next_step_inner_rank]:
                    dict_digit[digit] -= 1
            inner_rank = next_step_inner_rank + num_rank + 1
            is_addition = not is_addition
        num_to_ret += compute_resulting_num_dict_digit(dict_digit)
        print(f"we got one number for the chain, it is {num_to_ret}")
    return num_to_ret


next_phase_input = input_str * 10000
for _ in range(100):
    print(f"phase {_} done")
    print(f"param: {next_phase_input}")
    next_phase_input = apply_one_phase_on_num(next_phase_input)
    # print(next_phase_input)

# 09012683 too low
# 05350576 too low
offset = int(next_phase_input[:7])
print(next_phase_input[offset:offset + 8])
