# copypasted from https://stackoverflow.com/a/32481015/7059810
from typing import Union


def range_subset(range1: range, range2: range) -> bool:
    """Whether range1 is a subset of range2."""
    if not range1:
        return True  # empty range is subset of anything
    if not range2:
        return False  # non-empty range can't be subset of empty range
    if len(range1) > 1 and range1.step % range2.step:
        return False  # must have a single value or integer multiple step
    return range1.start in range2 and range1[-1] in range2


# copypasted from https://stackoverflow.com/a/6821298/7059810
def range_overlap(range1: range, range2: range) -> Union[range, None]:
    """Whether range1 is a subset of range2."""
    range_to_ret = range(max(range1[0], range2[0]), min(range1[-1], range2[-1])+1)
    return None if len(range_to_ret) == 0 else range_to_ret
