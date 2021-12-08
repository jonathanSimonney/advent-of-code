def parse_content(line_to_parse: str) -> dict:
    line_as_list = line_to_parse.split(" | ")
    list_all_digits = line_as_list[0].split(" ")
    list_output_digits = line_as_list[1].split(" ")
    return {"list_all_digits": list_all_digits, "list_output_digits": list_output_digits}


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [parse_content(line.strip()) for line in content]

nb_easy_output = 0

for dict_content in content:
    for output_digit in dict_content["list_output_digits"]:
        if len(output_digit) in [2, 3, 4, 7]:
            nb_easy_output += 1

# 508 too low
print(nb_easy_output)
