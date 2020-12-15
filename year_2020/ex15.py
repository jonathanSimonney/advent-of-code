def say_number(num_to_say, dict_numbers_spoken):
    ...


# list_starting_nums = [0, 3, 6]
list_starting_nums = [6, 19, 0, 5, 7, 13, 1]

dict_spoken_nbers = {}

nb_spoken_nums = -1
last_spoken_num = None

while nb_spoken_nums <= 30000000 - 2:
    nb_spoken_nums += 1
    if nb_spoken_nums < len(list_starting_nums):
        nb_to_say = list_starting_nums[nb_spoken_nums]
    elif last_spoken_num in dict_spoken_nbers:
        # the -1 is because it's the diff with the turn ON WHICH THAT NUMBER WAS TOLD, i.e, the nb of the turn right before
        nb_to_say = nb_spoken_nums - 1 - dict_spoken_nbers[last_spoken_num]
    else:
        nb_to_say = 0

    if last_spoken_num is not None:
        dict_spoken_nbers[last_spoken_num] = nb_spoken_nums - 1
    last_spoken_num = nb_to_say

print(last_spoken_num)
