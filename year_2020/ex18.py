def compute_line_total(line_str):
    current_op = "add"
    total = 0
    closing_parenthesis_index = None

    list_expressions = line_str.split(" ")
    str_index_pointer = 0

    for idx, group in enumerate(list_expressions):
        if closing_parenthesis_index is not None and str_index_pointer < closing_parenthesis_index:
            str_index_pointer += len(group) + 1
            continue
        if group == "+":
            current_op = "add"
        elif group == "*":
            current_op = "mult"
        else:
            if group[0] == '(':
                closing_parenthesis_index = line_str.find(')', str_index_pointer)
                while line_str[str_index_pointer + 1:closing_parenthesis_index].count("(") != line_str[str_index_pointer + 1:closing_parenthesis_index].count(")"):
                    closing_parenthesis_index = line_str.find(')', closing_parenthesis_index + 1)
                #     print(f"new closing parenthesis index found, {closing_parenthesis_index}")
                #
                # print(f"will now handle following str : {line_str[str_index_pointer + 1:closing_parenthesis_index]}")
                # print(closing_parenthesis_index)
                nb_to_handle = compute_line_total(line_str[str_index_pointer + 1:closing_parenthesis_index])
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

# print(compute_line_total("2 * 3 + (4 * 5)"))
# print(compute_line_total("5 + (8 * 3 + 9 + 3 * 4 * 3)"))
# print(compute_line_total("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"))
# print(compute_line_total("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"))

print(sum(list_total))
