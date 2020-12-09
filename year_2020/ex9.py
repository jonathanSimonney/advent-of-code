def any_2_number_has_sum(array_candidate, number_to_check):
    for i in array_candidate:
        for j in array_candidate:
            if i + j == number_to_check:
                return True

    return False


def get_first_invalid_number(list_numbers, preamble_len):
    for index, number in enumerate(list_numbers):
        if index < preamble_len:
            continue
        if not any_2_number_has_sum(list_numbers[index - preamble_len:index], number):
            return number


def get_continuous_set_summing_to_num(list_numbers, num_to_sum_to):
    candidate_list = []

    for num in array_int:
        for candidate in candidate_list:
            candidate.append(num)
            if sum(candidate) == invalid_number:
                return candidate
        candidate_list.append([num])


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line

array_int = [int(x.strip()) for x in content]

invalid_number = get_first_invalid_number(array_int, 25)
print(invalid_number)

answer = get_continuous_set_summing_to_num(array_int, invalid_number)

#3514981 too low
print(min(answer) + max(answer))

