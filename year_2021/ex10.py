dict_opening_to_closing_char = {'(': ')', '{': '}', '<': '>', '[': ']'}


def find_first_invalid_char_closing(line_param: str) -> str:
    list_closing_char_expected: list[str] = []
    for char in line_param:
        if char in dict_opening_to_closing_char.keys():
            list_closing_char_expected.append(dict_opening_to_closing_char[char])
        else:
            expected_char = list_closing_char_expected.pop()
            if char != expected_char:
                return char

    return 'valid_line'


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [line.strip() for line in content]

dict_invalid_char_num = {')': 0, '}': 0, '>': 0, ']': 0, 'valid_line': 0}

for line in content:
    invalid_char = find_first_invalid_char_closing(line)
    dict_invalid_char_num[invalid_char] += 1

print(3 * dict_invalid_char_num[')'] +
      57 * dict_invalid_char_num[']'] +
      1197 * dict_invalid_char_num['}'] +
      25137 * dict_invalid_char_num['>']
      )
