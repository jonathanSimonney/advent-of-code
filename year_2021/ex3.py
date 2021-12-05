def recursively_find_rating_in_list(
        list_binary_num: list[str],
        currently_checked_pos: int,
        take_most_common: bool) -> str:
    if len(list_binary_num) == 1:
        return list_binary_num[0]

    nb_1_minus_nb_0 = 0
    list_binary_num_with_1 = []
    list_binary_num_with_0 = []
    for single_num in list_binary_num:
        if single_num[currently_checked_pos] == '1':
            nb_1_minus_nb_0 += 1
            list_binary_num_with_1.append(single_num)
        else:
            nb_1_minus_nb_0 -= 1
            list_binary_num_with_0.append(single_num)

    if take_most_common:
        considered_list = list_binary_num_with_1 if nb_1_minus_nb_0 >= 0 else list_binary_num_with_0
    else:
        considered_list = list_binary_num_with_0 if nb_1_minus_nb_0 >= 0 else list_binary_num_with_1

    return recursively_find_rating_in_list(considered_list, currently_checked_pos + 1, take_most_common)





with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

# part 1
# dict_nb_1_minus_nb_0_per_pos: dict = collections.defaultdict(lambda: 0)
#
# for bin_str in content:
#     for idx, char in enumerate(bin_str):
#         if char == '1':
#             dict_nb_1_minus_nb_0_per_pos[idx] += 1
#         else:
#             dict_nb_1_minus_nb_0_per_pos[idx] -= 1
#
#
# acc_bin_gamma_str = ''
# acc_bin_epsilon_str = ''
# for nb_one in dict_nb_1_minus_nb_0_per_pos.values():
#     if nb_one > 0:
#         acc_bin_gamma_str += '1'
#         acc_bin_epsilon_str += '0'
#     else:
#         acc_bin_gamma_str += '0'
#         acc_bin_epsilon_str += '1'
#
# print(int(acc_bin_gamma_str, 2), acc_bin_gamma_str)
# print(int(acc_bin_gamma_str, 2) * int(acc_bin_epsilon_str, 2))

# part 2
print(
    int(recursively_find_rating_in_list(content, 0, True), 2) *
    int(recursively_find_rating_in_list(content, 0, False), 2))
