import collections
import copy
import math


def compute_dict_chemical(chemical_str):
    chemical_array = chemical_str.split(" ")
    produced_chemical_name = chemical_array[1]
    produced_chemical_quantity = int(chemical_array[0])
    return {'quantity': produced_chemical_quantity, 'name': produced_chemical_name}


def append_line_to_reactions(line_to_append, dict_reactions_to_fill):
    reaction_array = line_to_append.split(" => ")
    produced_chemical_dict = compute_dict_chemical(reaction_array[1])
    list_reactives = [compute_dict_chemical(reactive) for reactive in reaction_array[0].split(", ")]
    dict_reactions_to_fill[produced_chemical_dict['name']] = {
        'nb_produced': produced_chemical_dict['quantity'],
        'reactives': list_reactives
    }


def run_reaction_nb_time(chemical_to_produce, nb_time_reaction_ran, dict_reactions_filled):
    global dict_remaining_chemicals
    global dict_needed_chemicals
    reactives_needed = dict_reactions_filled[chemical_to_produce]['reactives']
    for reactive in reactives_needed:
        dict_needed_chemicals[reactive['name']] += nb_time_reaction_ran * reactive['quantity']
    dict_remaining_chemicals[chemical_to_produce] += \
        dict_reactions_filled[chemical_to_produce]['nb_produced'] * nb_time_reaction_ran


def produce_chemical(chemical_to_produce, needed_amount, dict_reactions_filled):
    nb_produced_by_reaction = dict_reactions_filled[chemical_to_produce]['nb_produced']
    nb_time_to_run_reaction = math.ceil(needed_amount / nb_produced_by_reaction)
    run_reaction_nb_time(chemical_to_produce, nb_time_to_run_reaction, dict_reactions_filled)


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

# expected format :
# {'FUEL':
#   {'nb_produced': 1, 'reactives': [
#       {'quantity': 3, 'name': 'RESG'}
#   ]}
# }
dict_reactions = {}
for line in content:
    append_line_to_reactions(line, dict_reactions)

dict_remaining_chemicals = collections.defaultdict(lambda:  0)
dict_needed_chemicals = collections.defaultdict(lambda:  0)
print(dict_reactions)
produce_chemical('FUEL', 1, dict_reactions)
while list(dict_needed_chemicals.keys()) != ['ORE']:
    for reactive_name in copy.deepcopy(dict_needed_chemicals).keys():
        if reactive_name != 'ORE':
            # accessing directly to keys avoid producing too much chemical because the same reactive was
            # ALREADY needed one time more
            amount_already_produced = min(dict_remaining_chemicals[reactive_name], dict_needed_chemicals[reactive_name])
            dict_needed_chemicals[reactive_name] -= amount_already_produced
            dict_remaining_chemicals[reactive_name] -= amount_already_produced
            if dict_needed_chemicals[reactive_name] != 0:
                produce_chemical(reactive_name, dict_needed_chemicals[reactive_name], dict_reactions)

    dict_needed_chemicals = collections.defaultdict(lambda: 0,
                                                    {k: v for k, v in dict_needed_chemicals.items() if v != 0})

# problem is we produced some chemicals even though we didn't need them I bet
# 371216 too low
# 444691 too high
print(dict_needed_chemicals['ORE'])
