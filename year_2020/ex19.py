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


def is_message_valid_with_v2_rules(message_to_check, dict_rules_finals):
    set_matchs_42 = dict_rules_finals[42]["must_match"]
    set_matchs_31 = dict_rules_finals[31]["must_match"]
    if message_to_check[:8] not in set_matchs_42:
        return False
    if message_to_check[8:16] not in set_matchs_42:
        return False
    if message_to_check[-8:] not in set_matchs_31:
        return False
    str_in_excess_to_compute = message_to_check[16:-8]
    if str_in_excess_to_compute == "":
        return True
    nb_found_42 = 0
    while True:
        try:
            if str_in_excess_to_compute[:8] in set_matchs_42:
                nb_found_42 += 1
                str_in_excess_to_compute = str_in_excess_to_compute[8:]
                if str_in_excess_to_compute == "":
                    return True
            else:
                break
        except IndexError:
            # given all match are of same len and no extra is allowed, if len isn't multiple of 8, it CAN'T possibly match
            return False
    for _ in range(nb_found_42):
        try:
            if str_in_excess_to_compute[:8] in set_matchs_31:
                str_in_excess_to_compute = str_in_excess_to_compute[8:]
                if str_in_excess_to_compute == "":
                    return True
            else:
                break
        except IndexError:
            # given all match are of same len and no extra is allowed, if len isn't multiple of 8, it CAN'T possibly match
            return False

    return False

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

# le remplacement équivaut à "au moins 2 * 42, mais autant de 42 qu'on veut, puis autant de 31 qu'on veut, mais max n_42 - 1 de 31"

acc = 0
for message in list_messages:
    if is_message_valid_with_v2_rules(message, dict_rules):
        acc += 1

print(acc)
