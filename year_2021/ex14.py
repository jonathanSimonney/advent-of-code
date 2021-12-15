import collections


def apply_transformations_to_polymer(
        dict_transformations: dict,
        dict_nb_polymers: dict
) -> dict:
    new_dict_nb_polymers = collections.defaultdict(lambda: 0)
    for polymer, nb_polymer in dict_nb_polymers.items():
        new_dict_nb_polymers[dict_transformations[polymer][0]] += nb_polymer
        new_dict_nb_polymers[dict_transformations[polymer][1]] += nb_polymer

    return new_dict_nb_polymers


def main():
    with open("data.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [line.strip() for line in content]

    current_polymer: str = content[0]
    dict_transformations: dict = {}

    for line in content[2:]:
        splitted_line = line.split(" -> ")
        dict_transformations[splitted_line[0]] = [splitted_line[0][0] + splitted_line[1], splitted_line[1] + splitted_line[0][1]]

    dict_nb_polymers = collections.defaultdict(lambda: 0)

    old_char = None
    for char in current_polymer:
        if old_char is not None:
            dict_nb_polymers[old_char + char] += 1
        old_char = char

    print(dict_nb_polymers)
    for _ in range(40):
        dict_nb_polymers = apply_transformations_to_polymer(dict_transformations, dict_nb_polymers)

    polymer_counter: dict = collections.defaultdict(lambda: 0)
    for polymer_str, nb_polymer in dict_nb_polymers.items():
        polymer_counter[polymer_str[0]] += nb_polymer
    polymer_counter[current_polymer[-1]] += 1
    print(max(polymer_counter.values()) - min(polymer_counter.values()))


if __name__ == "__main__":
    main()

# bnb
# bbnbb
# bn bbnbb nb
# bbnb b nbbnbbn b bnbb

# hh
# hcnch
# hbccnbcbh
