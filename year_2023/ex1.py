from typing import List


def get_n_th_digit_in_str(str_param: str, n_th_digit: int) -> str:
    str_param = (str_param
                 .replace("one", "one1one")
                 .replace("two", "two2two")
                 .replace("three", "three3three")
                 .replace("four", "four4four")
                 .replace("five", "five5five")
                 .replace("six", "six6six")
                 .replace("seven", "seven7seven")
                 .replace("eight", "eight8eight")
                 .replace("nine", "nine9nine")
                 )

    if n_th_digit == 0:
        raise AttributeError("n_th_digit cannot be equals to 0")
    elif n_th_digit < 0:
        str_param = str_param[::-1]
        n_th_digit = -n_th_digit

    idx_digit_found = 0
    for char in str_param:
        if char.isdigit():
            idx_digit_found += 1
            if idx_digit_found == n_th_digit:
                return char
    raise AssertionError(f"{n_th_digit} not found in str {str_param}")


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
# content = [parse_line_content(x) for x in content]

acc: int = 0
list_cal_values: List[int] = []

for line in content:
    list_cal_values.append(
        int(get_n_th_digit_in_str(line, 1) + get_n_th_digit_in_str(line, -1))
    )

# 53706 too low
print(sum(list_cal_values))
