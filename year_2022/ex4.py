import string
from typing import List

from common_helpers.range_helper import range_subset, range_overlap
from common_helpers.str_helpers import split_str_in_half


def parse_range(range_str) -> range:
    splitted_range_str = range_str.split('-')
    return range(int(splitted_range_str[0]), int(splitted_range_str[1]) + 1)


def parse_line_content(line_to_parse: str) -> list[range]:
    splitted_line = line_to_parse.split(',')
    return [parse_range(splitted_line[0]), parse_range(splitted_line[1])]


with open("data.txt") as f:
    content = [parse_line_content(x.strip()) for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line
# content = [parse_line_content(x) for x in content]

acc: int = 0


for line in content:
    if range_overlap(line[0], line[1]) is not None or range_overlap(line[1], line[0]) is not None:
        acc += 1

print(acc)
