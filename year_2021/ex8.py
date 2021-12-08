def get_missing_segment(bigger_digit_segments: str, smaller_digit_segments: str) -> str:
    result = bigger_digit_segments
    for digit in smaller_digit_segments:
        result = result.replace(digit, "")

    return result


def parse_content(line_to_parse: str) -> int:
    line_as_list = line_to_parse.split(" | ")
    list_all_digits = line_as_list[0].split(" ")
    list_output_digits = line_as_list[1].split(" ")

    dict_digit_segment_to_num = {}
    for digit in list_all_digits.copy():
        if len(digit) == 2:
            segments_one = ''.join(sorted(digit))
            dict_digit_segment_to_num[segments_one] = 1
            list_all_digits.remove(digit)
        elif len(digit) == 3:
            segments_seven = ''.join(sorted(digit))
            dict_digit_segment_to_num[segments_seven] = 7
            list_all_digits.remove(digit)
        elif len(digit) == 4:
            segments_four = ''.join(sorted(digit))
            dict_digit_segment_to_num[segments_four] = 4
            list_all_digits.remove(digit)
        elif len(digit) == 7:
            segments_eight = ''.join(sorted(digit))
            dict_digit_segment_to_num[segments_eight] = 8
            list_all_digits.remove(digit)

    for digit_segment_str in list_all_digits.copy():
        if len(digit_segment_str) == 6 and get_missing_segment(segments_eight, digit_segment_str) not in segments_four:
            segments_nine = ''.join(sorted(digit_segment_str))
            dict_digit_segment_to_num[segments_nine] = 9
            list_all_digits.remove(digit_segment_str)

    bottom_left_segment = get_missing_segment(segments_eight, segments_nine)
    for digit_segment_str in list_all_digits.copy():
        if len(digit_segment_str) == 5 and bottom_left_segment in digit_segment_str:
            segments_two = ''.join(sorted(digit_segment_str))
            dict_digit_segment_to_num[segments_two] = 2
            list_all_digits.remove(digit_segment_str)
        elif len(digit_segment_str) == 6:
            if get_missing_segment(segments_eight, digit_segment_str) in segments_seven:
                segments_six = ''.join(sorted(digit_segment_str))
                dict_digit_segment_to_num[segments_six] = 6
                list_all_digits.remove(digit_segment_str)
            else:
                segments_zero = ''.join(sorted(digit_segment_str))
                dict_digit_segment_to_num[segments_zero] = 0
                list_all_digits.remove(digit_segment_str)

    top_right_segment = get_missing_segment(segments_eight, segments_six)
    for digit_segment_str in list_all_digits:
        if top_right_segment in digit_segment_str:
            dict_digit_segment_to_num[''.join(sorted(digit_segment_str))] = 3
        else:
            dict_digit_segment_to_num[''.join(sorted(digit_segment_str))] = 5

    str_acc = ""
    for output_digit_segment in list_output_digits:
        str_acc += str(dict_digit_segment_to_num[''.join(sorted(output_digit_segment))])
    return int(str_acc)


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [parse_content(line.strip()) for line in content]

#977346 too low
print(sum(content))