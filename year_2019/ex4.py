def is_candidate_valid(candidate):
    previous_digit = -1
    found_a_double_digit = False
    is_double_digit_validated = False
    current_double_digit = -1
    for digit in str(candidate):
        if int(digit) < previous_digit:
            return False
        if int(digit) == current_double_digit:
            found_a_double_digit = False
            continue
        else:
            current_double_digit = -1
            is_double_digit_validated = found_a_double_digit or is_double_digit_validated
        if int(digit) == previous_digit:
            found_a_double_digit = True
            current_double_digit = previous_digit

        previous_digit = int(digit)
    return found_a_double_digit or is_double_digit_validated


min_number = 193651
max_number = 649729

# print(is_candidate_valid(557779))

nb_valid = 0
for candidate in range(min_number, max_number):
    if is_candidate_valid(candidate):
        nb_valid += 1

# 1633 too high, 924 too low, 1050 also too low
print(nb_valid)
