import math


def compute_number_from_binary_str(str_to_parse, char_lower, char_upper):
    min_pos = 0
    max_pos = math.pow(2, len(str_to_parse))
    for single_char in str_to_parse:
        new_val = (max_pos + min_pos) / 2
        if single_char == char_lower:
            max_pos = new_val
        elif single_char == char_upper:
            min_pos = new_val
        else:
            raise ValueError("invalid char found in str", single_char)

    if min_pos != max_pos:
        if min_pos == int(min_pos):
            return min_pos
        return max_pos

    raise Exception("something is wrong in this algo")


def parse_seat_info(binary_str):
    dict_to_ret = {"row": compute_number_from_binary_str(binary_str[:7], "F", "B"),
                   "column": compute_number_from_binary_str(binary_str[7:], "L", "R")}
    dict_to_ret["id"] = dict_to_ret["row"] * 7 + dict_to_ret["column"]
    return dict_to_ret


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [parse_seat_info(x.strip()) for x in content]

print(max(content, key=lambda seat_as_dict: seat_as_dict["row"] * 7 + seat_as_dict["column"]))

