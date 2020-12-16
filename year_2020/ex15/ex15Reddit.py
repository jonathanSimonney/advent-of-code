import numpy as np
import time
from numba import njit
from numba import types
from numba.typed import Dict

# copied from https://www.reddit.com/r/adventofcode/comments/kdf85p/2020_day_15_solutions/gfzwcjm?utm_source=share&utm_medium=web2x&context=3

nums = np.array([6, 19, 0, 5, 7, 13, 1], dtype=np.int64)

@njit("int64(int64[:], int64)")
def day15(nums, N):
    last = np.full(N, -1, dtype=np.int64)
    for i, x in enumerate(nums[:-1]):
        last[x] = i
    buffer = nums[-1]
    for i in range(len(nums) - 1, N - 1):
        y = 0 if last[buffer] == -1 else i - last[buffer]
        last[buffer], buffer = i, y
    return buffer

# print(day15(nums, 2020))
t0 = time.time()
print(day15(nums, 30000000))

t1 = time.time()
# 20 seconds with njit annotation commented, less than 1 second otherwhise
print(t1 - t0)
