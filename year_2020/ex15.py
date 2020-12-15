import time

list_starting_nums = [6, 19, 0, 5, 7, 13, 1]

dict_spoken_nbers = {}

nb_spoken_nums = -1
last_spoken_num = None

max_treshold = 30000000 - 2

tLess1 = time.time()

for num in list_starting_nums:
    nb_spoken_nums += 1
    nb_to_say = list_starting_nums[nb_spoken_nums]
    if last_spoken_num is not None:
        dict_spoken_nbers[last_spoken_num] = nb_spoken_nums - 1
    last_spoken_num = nb_to_say

t0 = time.time()
print(t0 - tLess1)
for nb_spoken_nums in range(nb_spoken_nums, max_treshold + 1):
    try:
        nb_to_say = nb_spoken_nums - dict_spoken_nbers[last_spoken_num]
    except KeyError:
        nb_to_say = 0

    dict_spoken_nbers[last_spoken_num] = nb_spoken_nums
    last_spoken_num = nb_to_say

print(last_spoken_num)
t1 = time.time()
#
print(t1 - t0)
