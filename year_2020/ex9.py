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
    min_index = 0
    max_index = 0
    sum_tested = 0

    for num in list_numbers:
        max_index += 1
        sum_tested += num

        while sum_tested > num_to_sum_to:
            sum_tested -= list_numbers[min_index]
            min_index += 1
        if sum_tested == num_to_sum_to:
            return list_numbers[min_index:max_index]


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line

array_int = [int(x.strip()) for x in content]

invalid_number = get_first_invalid_number(array_int, 25)
print(invalid_number)

answer = get_continuous_set_summing_to_num(array_int, invalid_number)

print(min(answer) + max(answer))

