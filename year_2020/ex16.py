import itertools


# format of dict_where_rule_must_appear will be : {"class": [{"min": 1, "max": 3}, {"min": 5, "max": 7}]}
def parse_instruction_rule(dict_where_rule_must_appear, str_rule):
    array_infos = str_rule.split(": ")
    array_constraints_dicts = []

    key = array_infos[0]
    array_constraints = array_infos[1].split(" or ")
    for str_constraint in array_constraints:
        array_single_constraint = str_constraint.split("-")
        array_constraints_dicts.append({"min": int(array_single_constraint[0]), "max": int(array_single_constraint[1])})

    dict_where_rule_must_appear[key] = array_constraints_dicts


def check_validity_against_single_constraint(value_to_check, single_constraint):
    return single_constraint["min"] <= value_to_check <= single_constraint["max"]


def check_validity_against_array_constraints(value_to_check, list_constraints):
    for constraint in list_constraints:
        if check_validity_against_single_constraint(value_to_check, constraint):
            return True

    return False


def get_all_invalid_values_in_ticket(list_values, dict_rule_to_check):
    list_invalid_values = []

    for value in list_values:
        valid_for_at_least_one_constraint = False
        for constraint_lists in dict_rule_to_check.values():
            if check_validity_against_array_constraints(value, constraint_lists):
                valid_for_at_least_one_constraint = True
                break
        if not valid_for_at_least_one_constraint:
            list_invalid_values.append(value)

    return list_invalid_values


def find_constraint_valid_for_idx(dict_rule_to_check, list_tickets_to_check_against, idx_to_check):
    list_possibles_rule_name = []

    for rule_name, rule_array in dict_rule_to_check.items():
        all_tickets_are_ok_with_this_rule = True
        for valid_ticket in list_tickets_to_check_against:
            if not check_validity_against_array_constraints(valid_ticket[idx_to_check], rule_array):
                all_tickets_are_ok_with_this_rule = False
                break
        if all_tickets_are_ok_with_this_rule:
            list_possibles_rule_name.append(rule_name)

    return list_possibles_rule_name


with open("data.txt") as f:
    list_instruction = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line

dict_rules = {}
own_ticket = []
list_nearby_tickets = []

all_rules_parsed = False
own_ticket_parsed = False

for line in list_instruction:
    if line == "":
        if not all_rules_parsed:
            all_rules_parsed = True
        else:
            own_ticket_parsed = True
        continue
    if not all_rules_parsed:
        parse_instruction_rule(dict_rules, line)
    else:
        if ":" in line:
            continue
        elif not own_ticket_parsed:
            own_ticket = [int(x) for x in line.split(",")]
        else:
            list_nearby_tickets.append([int(x) for x in line.split(",")])

# part 1
# error_rate = 0
# for ticket in list_nearby_tickets:
#     error_rate += sum(get_all_invalid_values_in_ticket(ticket, dict_rules))
#
# #2273544 too high
# print(error_rate)

# part 2
list_valid_tickets = []

for ticket in list_nearby_tickets:
    if not get_all_invalid_values_in_ticket(ticket, dict_rules):
        list_valid_tickets.append(ticket)

list_valid_tickets.append(own_ticket)

order_fields_possibilities = {}

for i in range(len(own_ticket)):
    possible_rule_name_list = find_constraint_valid_for_idx(dict_rules, list_valid_tickets, i)
    order_fields_possibilities[i] = possible_rule_name_list

dict_unique_found_fields = {}
set_found_fields = set()

while len(dict_unique_found_fields) != len(own_ticket):
    for idx, list_rules_name in order_fields_possibilities.items():
        order_fields_possibilities[idx] = list(filter(lambda x: x not in set_found_fields, list_rules_name))
        if len(order_fields_possibilities[idx]) == 1:
            dict_unique_found_fields[idx] = order_fields_possibilities[idx]
            set_found_fields.add(order_fields_possibilities[idx][0])

order_fields_as_list = []

for i in range(len(own_ticket)):
    order_fields_as_list.append(dict_unique_found_fields[i][0])

answer = 1
for idx, name_field in enumerate(order_fields_as_list):
    if name_field.split(" ")[0] == "departure":
        answer *= own_ticket[idx]

# 559708174747 too low
# 2424503013148311563411 too high
print(answer)

# print(find_constraint_valid_for_idx(dict_rules, list_valid_tickets, 0))
