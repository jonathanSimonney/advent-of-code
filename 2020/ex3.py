with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]


def check_input_with_slope(right, down):
    index_to_look_at = 0
    line_len = len(content[0])
    nb_tree_on_road = 0
    nb_down = -1
    for line in content[1:]:
        index_to_look_at += right
        nb_down += 1

        if nb_down % down != 0:
            continue
        if line[index_to_look_at % line_len] == "#":
            nb_tree_on_road += 1
    return nb_tree_on_road


print(check_input_with_slope(1, 1))
print(check_input_with_slope(3, 1))
print(check_input_with_slope(5, 1))
print(check_input_with_slope(7, 1))
print(check_input_with_slope(1, 2))
print(
    check_input_with_slope(1, 1) * check_input_with_slope(3, 1) * check_input_with_slope(5, 1) * check_input_with_slope(
        7, 1) * check_input_with_slope(1, 2))
