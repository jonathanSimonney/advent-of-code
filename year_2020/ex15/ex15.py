import time
import array

# list_starting_nums = [0, 3, 6]
list_starting_nums = [6, 19, 0, 5, 7, 13, 1]

list_spoken_nbers = array.array('i', (-1,)*30000000)
tLess1 = time.time()

for idx, num in enumerate(list_starting_nums[:-1]):
    list_spoken_nbers[num] = idx

# nb_spoken_nums = -1
last_spoken_num = list_starting_nums[-1]

max_treshold = 30000000

t0 = time.time()
print(t0 - tLess1)
range_to_iterate_on = range(len(list_starting_nums) - 1, max_treshold - 1)
for nb_spoken_nums in range_to_iterate_on:

    if list_spoken_nbers[last_spoken_num] == -1:
        current_spoken_num = 0
    else:
        current_spoken_num = nb_spoken_nums - list_spoken_nbers[last_spoken_num]

    list_spoken_nbers[last_spoken_num] = nb_spoken_nums

    last_spoken_num = current_spoken_num


print(last_spoken_num)
t1 = time.time()
# approx 10 seconds
print(t1 - t0)
