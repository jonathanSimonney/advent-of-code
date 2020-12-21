import collections


def add_line_to_dict(line_to_add, list_all_ingredients):
    splitted_line = line_to_add.split(" (contains ")
    list_ingredient = splitted_line[0].split(" ")
    list_all_ingredients += list_ingredient

    list_allergens = splitted_line[1].replace(")", "").split(", ")
    for allergen in list_allergens:
        dict_allergens_possibilities[allergen].append(list_ingredient)


with open("data.txt") as f:
    content = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line
dict_allergens_possibilities = collections.defaultdict(lambda:  [])
list_ingredients = []

for line in content:
    add_line_to_dict(line, list_ingredients)

dict_unique_allergens = {}
found_new_allergen = True

while found_new_allergen:
    found_new_allergen = False
    set_food_found_allergen = set([food_name for food_name in dict_unique_allergens])
    for allergen, matrice_food in dict_allergens_possibilities.items():
        set_food_list = set(matrice_food[0])
        for food_list in matrice_food:
            set_food_list = set_food_list.intersection(food_list).difference(set_food_found_allergen)

        if len(set_food_list) == 1:
            found_new_allergen = True
            food_name = list(set_food_list)[0]
            dict_unique_allergens[food_name] = allergen

acc = 0

for ingredient in list_ingredients:
    if ingredient not in dict_unique_allergens.keys():
        acc += 1

# 4909 too high
print(acc)

# thanks to https://stackoverflow.com/a/613218/7059810
dict_unique_allergen_sorted_by_allergen = dict(sorted(dict_unique_allergens.items(), key=lambda item: item[1]))

acc = ""
for food_name in dict_unique_allergen_sorted_by_allergen.keys():
    acc += "," + food_name
print(acc)
