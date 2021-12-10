from statistics import median

dict_opening_to_closing_char = {'(': ')', '{': '}', '<': '>', '[': ']'}


def compute_line_score(line_to_compute) -> int:
    dict_completion_char_score = {')': 1, '}': 3, '>': 4, ']': 2}

    acc = 0
    for char in line_to_compute:
        acc *= 5
        acc += dict_completion_char_score[char]
    return acc


def find_first_invalid_char_closing_or_needed_completion_line(line_param: str) -> str:
    list_closing_char_expected: list[str] = []
    for char in line_param:
        if char in dict_opening_to_closing_char.keys():
            list_closing_char_expected.append(dict_opening_to_closing_char[char])
        else:
            expected_char = list_closing_char_expected.pop()
            if char != expected_char:
                return char

    list_closing_char_expected.reverse()
    return ''.join(list_closing_char_expected)


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [line.strip() for line in content]

dict_invalid_char_num = {')': 0, '}': 0, '>': 0, ']': 0}
list_completion_line_score: list[int] = []

for line in content:
    invalid_char_or_completion_line = find_first_invalid_char_closing_or_needed_completion_line(line)
    if invalid_char_or_completion_line in dict_invalid_char_num.keys():
        dict_invalid_char_num[invalid_char_or_completion_line] += 1
    else:
        list_completion_line_score.append(compute_line_score(invalid_char_or_completion_line))

print(3 * dict_invalid_char_num[')'] +
      57 * dict_invalid_char_num[']'] +
      1197 * dict_invalid_char_num['}'] +
      25137 * dict_invalid_char_num['>']
      )

# 4144007457 too high
list_completion_line_score.sort()
print(median(list_completion_line_score))
