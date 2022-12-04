import string
from typing import List

from common_helpers.str_helpers import split_str_in_half


def compute_letter_score(letter: str) -> int:
    lowercase_letter_score: int = string.ascii_lowercase.index(letter.lower()) + 1
    if letter.islower():
        return lowercase_letter_score
    return lowercase_letter_score + 26


with open("data.txt") as f:
    content = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line
# content = [parse_line_content(x) for x in content]

acc: int = 0

group_list: list[str] = []

for line in content:
    group_list.append(line)
    if len(group_list) == 3:
        common_elem_list = list(set(group_list[0]).intersection(group_list[1]).intersection(group_list[2]))
        acc += compute_letter_score(common_elem_list[0])
        group_list = []

print(acc)
