import collections
import string
from typing import List

from common_helpers.range_helper import range_subset, range_overlap
from common_helpers.str_helpers import split_str_in_half


class CratePiles:
    crate_list: dict[int, list[str]]

    def __init__(self):
        self.crate_list = collections.defaultdict(lambda: [])

    def _add_crate_to_pile_top(self, idx_pile: int, crate_id: str):
        self.crate_list[idx_pile].append(crate_id)

    def move_n_crate_between_pile(self, nb_crate_moved, origin_pile, arrival_pile):
        for _ in range(nb_crate_moved):
            self.move_one_crate_between_pile(origin_pile, arrival_pile)

    def move_one_crate_between_pile(self, from_pile, to_pile):
        crate_moved_id = self.crate_list[from_pile].pop()
        self.crate_list[to_pile].append(crate_moved_id)


with open("data.txt") as f:
    content = [parse_line_content(x.strip()) for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line
# content = [parse_line_content(x) for x in content]

acc: int = 0


for line in content:
    if range_overlap(line[0], line[1]) is not None or range_overlap(line[1], line[0]) is not None:
        acc += 1

print(acc)
