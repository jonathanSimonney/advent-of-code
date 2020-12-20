# def is_str_valid_with_rule(dict_to_check_against, rule_idx, str_to_check):
#     rule = dict_to_check_against[rule_idx]
#     if rule["is_final"]:
#         if str_to_check[0] == rule["must_match"]:
#             try:
#                 return {"is_valid": True, "left_str": str_to_check[1:]}
#             except IndexError:
#                 return {"is_valid": True, "left_str": ""}
#     for list_rules_to_check in rule["must_match"]:
#         is_current_list_rules_valid = True
#         for rule_key in list_rules_to_check:
import itertools


def compute_list_valid_strs(dict_to_make_final, list_rule_numbers):
    first_rule_number = list_rule_numbers[0]
    set_strs_valids = dict_to_make_final[first_rule_number]["must_match"]

    if len(list_rule_numbers) > 1:
        for rule_number in list_rule_numbers[1:]:
            new_set_strs_valids = set()

            for valid_str in dict_to_make_final[rule_number]["must_match"]:
                for old_valid_str in set_strs_valids:
                    new_set_strs_valids.add(old_valid_str + valid_str)

            set_strs_valids = new_set_strs_valids

    return set_strs_valids


def make_directory_rules_final(dict_to_make_final):
    set_final_keys = set()
    while len(set_final_keys) != len(dict_to_make_final):
        for key, rule in dict_to_make_final.items():
            if rule["is_final"]:
                set_final_keys.add(key)
            else:
                flattened_rules = itertools.chain.from_iterable(rule["must_match"])
                can_rule_become_final = all(x in set_final_keys for x in flattened_rules)
                if can_rule_become_final:
                    set_matches = set()
                    # new_rule = {"is_final": True, "must_match": []}
                    for list_rule_numbers in rule["must_match"]:
                        set_matches.update(compute_list_valid_strs(dict_to_make_final, list_rule_numbers))
                    dict_to_make_final[key] = {"is_final": True, "must_match": set_matches}
                    set_final_keys.add(key)





def add_rule_to_dict(str_rule, dict_to_fill):
    array_rule = str_rule.split(": ")
    key = int(array_rule[0])
    if array_rule[1][0] == "\"":
        value = {"is_final": True, "must_match": set(array_rule[1][1])}
    else:
        list_possible_rules = array_rule[1].split(" | ")
        value = {"is_final": False, "must_match": []}
        for rule in list_possible_rules:
            list_ref_rule = [int(x) for x in rule.split(" ")]
            value["must_match"].append(list_ref_rule)

    dict_to_fill[key] = value


with open("data.txt") as f:
    content = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line

dict_rules = {}

for idx, line in enumerate(content):
    if line == "":
        break
    add_rule_to_dict(line, dict_rules)

list_messages = content[idx+1:]
print(list_messages[0])

make_directory_rules_final(dict_rules)

print(dict_rules[42]["must_match"])
print(dict_rules[31]["must_match"])
print(dict_rules[8]["must_match"])
print(dict_rules[11]["must_match"])

acc = 0
for message in list_messages:
    if message in dict_rules[0]["must_match"]:
        acc += 1

print(acc)
