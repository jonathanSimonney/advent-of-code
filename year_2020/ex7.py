def parse_line_content(str_line, acc_dict):
    line_array = str_line.split(" contain ")
    color_key = line_array[0].replace(" bags", "")
    color_value = {}

    if line_array[1] != "no other bags.":
        array_value = line_array[1].split(", ")
        for value_str in array_value:
            splitted_value = value_str.split(" ")
            quantity = int(splitted_value[0])
            color_name = " ".join(splitted_value[1:3])
            color_value[color_name] = quantity

    acc_dict[color_key] = color_value


def recursive_check_can_contain_bag(dict_bags_to_search, searched_bag, checked_bag):
    if dict_bags_to_search[checked_bag] == {}:
        return False

    contained_bags = dict_bags_to_search[checked_bag].keys()
    if searched_bag in contained_bags:
        return True

    for single_contained_bag in contained_bags:
        if recursive_check_can_contain_bag(dict_bags_to_search, searched_bag, single_contained_bag):
            return True

    return False


def recursive_count_contained_bag(dict_bags_to_search, searched_bag):
    nb_total_bags = 0
    if dict_bags_to_search[searched_bag] == {}:
        return 0
    for color, nb_bags in dict_bags_to_search[searched_bag].items():
        # the + 1 is for the container bag, which ALSO counts
        nb_total_bags += nb_bags * (recursive_count_contained_bag(dict_bags_to_search, color) + 1)

    return nb_total_bags


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line

dict_bags = {}
for x in content:
    parse_line_content(x.strip(), dict_bags)
# exemple of input workable :
# {"dark light red": {"golden shiny": 34, "faded blue": 3}, "faded blue": {}}

print(dict_bags)

nb_valid_bags = 0
for bag in dict_bags:
    if recursive_check_can_contain_bag(dict_bags, "shiny gold", bag):
        nb_valid_bags += 1

# 16436 too low
# 36625 too high
print(recursive_count_contained_bag(dict_bags, "shiny gold"))
