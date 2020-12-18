def compute_line_total(line_str):
    current_op = "add"
    total = 0
    closing_parenthesis_index = None
    closing_mult_group_index = None

    list_expressions = line_str.split(" ")
    str_index_pointer = 0

    for group in list_expressions:
        if (closing_parenthesis_index is not None and str_index_pointer < closing_parenthesis_index) or \
                (closing_mult_group_index is not None and str_index_pointer < closing_mult_group_index):
            str_index_pointer += len(group) + 1
            continue
        if group == "+":
            current_op = "add"
        elif group == "*":
            current_op = "mult"
            closing_mult_group_index = line_str.find('*', str_index_pointer + 2)
            sub_line_to_parse = line_str[str_index_pointer + 2:closing_mult_group_index - 1]

            while sub_line_to_parse.count("(") != sub_line_to_parse.count(")") and closing_mult_group_index != -1:
                closing_mult_group_index = line_str.find('*', closing_mult_group_index + 1)
                sub_line_to_parse = line_str[str_index_pointer + 2:closing_mult_group_index - 1]

            if closing_mult_group_index == -1:
                sub_line_to_parse = line_str[str_index_pointer + 2:]
                closing_mult_group_index = len(line_str)

            nb_to_handle = compute_line_total(sub_line_to_parse)
            total *= nb_to_handle
        else:
            if group[0] == '(':
                closing_parenthesis_index = line_str.find(')', str_index_pointer)
                sub_line_to_parse = line_str[str_index_pointer + 1:closing_parenthesis_index]

                while sub_line_to_parse.count("(") != sub_line_to_parse.count(")"):
                    closing_parenthesis_index = line_str.find(')', closing_parenthesis_index + 1)
                    sub_line_to_parse = line_str[str_index_pointer + 1:closing_parenthesis_index]
                nb_to_handle = compute_line_total(sub_line_to_parse)
            elif group[-1] == ')':
                raise ValueError("shouldn't reach a closing parenthesis, EVER")
            else:
                nb_to_handle = int(group)

            if current_op == "add":
                total += nb_to_handle
            elif current_op == "mult":
                total *= nb_to_handle

        str_index_pointer += len(group) + 1

    return total


with open("data.txt") as f:
    list_total = [compute_line_total(x.strip()) for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line

# print(compute_line_total("1 + (2 * 3) + (4 * (5 + 6))"))
# print(compute_line_total("5 + (8 * 3 + 9 + 3 * 4 * 3)"))
# print(compute_line_total("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"))
# print(compute_line_total("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"))

print(sum(list_total))
