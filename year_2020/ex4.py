
# note, if this becomes base for following exercise, take time to refacto, could do my char per char validation a bit
# better, AND factorised the whole is in interval comp. Should probably raise exception in singular small methods,
# and except them in the big method to refuse add to set. Also, je devrais passer par un dictionnaire de validateurs
# chaque valeur du dictionnaire est une fonction qui retourne un booléen
def add_field_to_set_if_valid(set_to_fill, field_info):
    field_info_array = field_info.split(":")
    field_name = field_info_array[0]
    field_value = field_info_array[1]
    if field_name == "byr":
        if int(field_value) < 1920 or int(field_value) > 2002:
            return

    if field_name == "iyr":
        if int(field_value) < 2010 or int(field_value) > 2020:
            return

    if field_name == "eyr":
        if int(field_value) < 2020 or int(field_value) > 2030:
            return

    if field_name == "hgt":
        suffix = field_value[-2:]
        try:
            height_num = int(field_value[:-2])
        except ValueError:
            return
        if suffix == "cm" and (height_num < 150 or height_num > 193):
            return
        if suffix == "in" and (height_num < 59 or height_num > 76):
            return
        if suffix != "cm" and suffix != "in":
            return

    if field_name == "hcl":
        if field_value[0] != "#":
            return
        if len(field_value[1:]) != 6:
            return
        for char in field_value[1:]:
            if char not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'}:
                return

    if field_name == "ecl" and field_value not in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
        return

    if field_name == "pid":
        if len(field_value) != 9:
            return
        for char in field_value[1:]:
            if char not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                return

    set_to_fill.add(field_name)


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

set_needed_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
set_found_field = set()
nb_valid_passport = 0

is_current_passport_valid = False
for line in content:
    if line == "":
        set_found_field = set()
        is_current_passport_valid = False
        continue
    list_line_info = line.split(" ")
    for single_info in list_line_info:
        add_field_to_set_if_valid(set_found_field, single_info)
    if (set_found_field.issuperset(set_needed_fields) or set_found_field == set_needed_fields) and not is_current_passport_valid:
        nb_valid_passport += 1
        is_current_passport_valid = True

# 107 too low
print(nb_valid_passport)
