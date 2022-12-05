import collections
import string
from typing import List, Dict


class CratePiles:
    crate_list: Dict[int, List[str]]

    def __init__(self):
        self.crate_list = collections.defaultdict(lambda: [])

        self.crate_list[0] = ['W', 'R', 'F']
        self.crate_list[1] = ['T', 'H', 'M', 'C', 'D', 'V', 'W', 'P']
        self.crate_list[2] = ['P', 'M', 'Z', 'N', 'L']
        self.crate_list[3] = ['J', 'C', 'H', 'R']
        self.crate_list[4] = list('CPGHQTB')
        self.crate_list[5] = list('GCWLFZ')
        self.crate_list[6] = list('WVLQZJGC')
        self.crate_list[7] = list('PNRFWTVC')
        self.crate_list[8] = list('JWHGRSV')

        # self.crate_list[0] = list('ZN')
        # self.crate_list[1] = list('MCD')
        # self.crate_list[2] = list('P')

    def _add_crate_to_pile_top(self, idx_pile: int, crate_id: str):
        self.crate_list[idx_pile].append(crate_id)

    def move_n_crate_between_pile(self, nb_crate_moved, origin_pile, arrival_pile):
        for _ in range(nb_crate_moved):
            self.move_one_crate_between_pile(origin_pile, arrival_pile)

    def move_one_crate_between_pile(self, origin_pile, arrival_pile):
        crate_moved_id = self.crate_list[origin_pile].pop()
        self.crate_list[arrival_pile].append(crate_moved_id)

    def get_system_result(self) -> string:
        return ''.join([crate_pile[-1] for crate_pile in self.crate_list.values()])


with open("data.txt") as f:
    content = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line
# content = [parse_line_content(x) for x in content]

crate_piles: CratePiles = CratePiles()

for line in content:
    splitted_line: List[str] = line.split(" ")
    try:
        if splitted_line[0] == 'move':
            nb_crates_moved = int(splitted_line[1])
            from_pile = int(splitted_line[3]) - 1
            to_pile = int(splitted_line[5]) - 1
            crate_piles.move_n_crate_between_pile(nb_crates_moved, from_pile, to_pile)
    except IndexError:
        continue

# FVCVPSCJTW wrong
print(crate_piles.get_system_result())
