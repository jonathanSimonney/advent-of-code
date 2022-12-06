import collections
from typing import Dict, Set


def add_char_to_set_at_idx(char_to_add: str, idx_set: int) -> bool:
    global dict_possibles_sets
    if char_to_add in dict_possibles_sets[idx_set]:
        dict_possibles_sets[idx_set] = set()
    dict_possibles_sets[idx_set].add(char_to_add)
    if len(dict_possibles_sets[idx_set]) == len_message_to_detect:
        return True
    return False


with open("data.txt") as f:
    content = f.read().splitlines()[0]

len_message_to_detect = 14

acc: int = 0
dict_possibles_sets: Dict[int, Set] = collections.defaultdict(lambda: set())

for char in content:
    should_stop: bool = False
    for i in range(len_message_to_detect):
        should_stop = add_char_to_set_at_idx(char, acc + i) or should_stop

    acc += 1
    if should_stop:
        break
# 4095 too high
print(acc)
