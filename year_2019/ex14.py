import collections
import copy
import math


def append_line_to_reactions(line_to_append, dict_reactions_to_fill):
    reaction_array = line_to_append.split(" => ")
    produced_chemical_dict = compute_dict_chemical(reaction_array[1])
    list_reactives = [compute_dict_chemical(reactive) for reactive in reaction_array[0].split(", ")]
    dict_reactions_to_fill[produced_chemical_dict['name']] = {
        'nb_produced': produced_chemical_dict['quantity'],
        'reactives': list_reactives
    }


def compute_dict_chemical(chemical_str):
    chemical_array = chemical_str.split(" ")
    produced_chemical_name = chemical_array[1]
    produced_chemical_quantity = int(chemical_array[0])
    return {'quantity': produced_chemical_quantity, 'name': produced_chemical_name}


def run_reaction_nb_time(chemical_to_produce, nb_time_reaction_ran, dict_reactions_filled):
    global dict_remaining_chemicals
    global dict_needed_chemicals
    reactives_needed = dict_reactions_filled[chemical_to_produce]['reactives']
    for reactive in reactives_needed:
        dict_needed_chemicals[reactive['name']] += nb_time_reaction_ran * reactive['quantity']
    dict_remaining_chemicals[chemical_to_produce] += \
        dict_reactions_filled[chemical_to_produce]['nb_produced'] * nb_time_reaction_ran


def revert_reaction_nb_time(chemical_to_revert, nb_time_reaction_reverted, dict_reactions_filled):
    global dict_remaining_chemicals
    global dict_needed_chemicals
    reactives_needed = dict_reactions_filled[chemical_to_revert]['reactives']
    for reactive in reactives_needed:
        dict_remaining_chemicals[reactive['name']] += nb_time_reaction_reverted * reactive['quantity']
    dict_remaining_chemicals[chemical_to_revert] -= \
        dict_reactions_filled[chemical_to_revert]['nb_produced'] * nb_time_reaction_reverted


def produce_chemical(chemical_to_produce, needed_amount, dict_reactions_filled):
    nb_produced_by_reaction = dict_reactions_filled[chemical_to_produce]['nb_produced']
    nb_time_to_run_reaction = math.ceil(needed_amount / nb_produced_by_reaction)
    run_reaction_nb_time(chemical_to_produce, nb_time_to_run_reaction, dict_reactions_filled)


def revert_production_chemical(chemical_to_revert, amount_chemical, dict_reactions_filled):
    nb_produced_by_reaction = dict_reactions_filled[chemical_to_revert]['nb_produced']
    nb_time_to_revert_reaction = math.floor(amount_chemical / nb_produced_by_reaction)
    revert_reaction_nb_time(chemical_to_revert, nb_time_to_revert_reaction, dict_reactions_filled)


def run_system_until_only_ore_needed():
    global dict_remaining_chemicals
    global dict_needed_chemicals
    while list(dict_needed_chemicals.keys()) != ['ORE']:
        for reactive_name in copy.deepcopy(dict_needed_chemicals).keys():
            if reactive_name != 'ORE':
                # accessing directly to keys avoid producing too much chemical because the same reactive was
                # ALREADY needed one time more
                amount_already_produced = min(dict_remaining_chemicals[reactive_name],
                                              dict_needed_chemicals[reactive_name])
                dict_needed_chemicals[reactive_name] -= amount_already_produced
                dict_remaining_chemicals[reactive_name] -= amount_already_produced
                if dict_needed_chemicals[reactive_name] != 0:
                    produce_chemical(reactive_name, dict_needed_chemicals[reactive_name], dict_reactions)

        dict_needed_chemicals = collections.defaultdict(lambda: 0,
                                                        {k: v for k, v in dict_needed_chemicals.items() if v != 0})


def run_system_until_no_excess_product_remains(dict_reactions_filled):
    global dict_remaining_chemicals
    global dict_needed_chemicals
    has_changes = True
    while has_changes:
        has_changes = False
        for reactive_name, reactive_amount in copy.deepcopy(dict_remaining_chemicals).items():
            if reactive_name != 'FUEL' and reactive_name != 'ORE' and reactive_amount >= dict_reactions_filled[reactive_name]['nb_produced']:
                has_changes = True
                revert_production_chemical(reactive_name, reactive_amount, dict_reactions_filled)


def produce_fuel_with_shortcut(nb_ore_input, nb_fuel_for_ore):
    global dict_remaining_chemicals
    global dict_needed_chemicals
    global dict_chemical_producted
    nb_time_can_rerun = math.floor(nb_ore_input / nb_fuel_for_ore)

    for chemical_name, chemical_amount in dict_chemical_producted.items():
        dict_remaining_chemicals[chemical_name] += nb_time_can_rerun * chemical_amount
    dict_needed_chemicals['ORE'] += nb_time_can_rerun * nb_fuel_for_ore


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
run_system_until_only_ore_needed()

# problem is we produced some chemicals even though we didn't need them I bet
# 371216 too low
# 444691 too high
# print(dict_needed_chemicals['ORE'])

# to get the result for THAT amount of ore, we'll need to put ALL the remaining non null chemical to make a key.
# This way we'll know when we reach a previously reached state
# and this mean we can go much faster to 1000000000000 ORE

# new rule ! we produce one ore, we then know how much ore is needed minimum for one fuel.
# 1. We'll do as much fuel as we can with this single ore (just use a division to know how much, and multiply ALL
# remaining chemicals,  and needed chemicals, by this result).
# 2. Then "revert" as many remaining chemicals as possible (except fuel, ofc). Repeat as long as you have
# reversions you can do
# 3. produce the fuel with the "ore per fuel" shortcut you already have for the diff between 1000000000000 and the
# amount ore you already used, and repeat step 2 as long as necessary
# 4. produce one fuel by one fuel and run the run_system_until_only_ore_needed until you go above the 1000000000000
# ORE limit.

# 1. We'll do as much fuel as we can with this single ore (just use a division to know how much, and multiply ALL
# remaining chemicals,  and needed chemicals, by this result).
min_ore_for_one_fuel = dict_needed_chemicals['ORE']
dict_chemical_producted = copy.deepcopy(dict_remaining_chemicals)
produce_fuel_with_shortcut(1000000000000 - min_ore_for_one_fuel, min_ore_for_one_fuel)

# 2. Then "revert" as many remaining chemicals as possible (except fuel, ofc). Repeat as long as you have
# reversions you can do
run_system_until_no_excess_product_remains(dict_reactions)

dict_needed_chemicals['ORE'] -= dict_remaining_chemicals['ORE']
dict_remaining_chemicals['ORE'] = 0
# 3. produce the fuel with the "ore per fuel" shortcut you already have for the diff between 1000000000000 and the
# amount ore you already used, and repeat step 2 as long as necessary
while 1000000000000 - dict_needed_chemicals['ORE'] >= min_ore_for_one_fuel:
    produce_fuel_with_shortcut(1000000000000 - dict_needed_chemicals['ORE'], min_ore_for_one_fuel)
    run_system_until_no_excess_product_remains(dict_reactions)
    dict_needed_chemicals['ORE'] -= dict_remaining_chemicals['ORE']
    dict_remaining_chemicals['ORE'] = 0


while dict_needed_chemicals['ORE'] < 1000000000000:
    produce_chemical('FUEL', 1, dict_reactions)
    run_system_until_only_ore_needed()
print(dict_remaining_chemicals['FUEL'] - 1)
