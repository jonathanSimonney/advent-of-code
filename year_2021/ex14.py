import collections


def apply_transformations_to_polymer(polymer_str: str, dict_transformations: dict) -> str:
    new_polymer = ''

    old_char = None
    for char in polymer_str:
        if old_char is not None:
            new_polymer += dict_transformations[old_char + char]
        new_polymer += char
        old_char = char

    return new_polymer


def main():
    with open("data.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [line.strip() for line in content]

    current_polymer: str = content[0]
    dict_transformations: dict = {}

    for line in content[2:]:
        splitted_line = line.split(" -> ")
        dict_transformations[splitted_line[0]] = splitted_line[1]

    for _ in range(40):
        current_polymer = apply_transformations_to_polymer(current_polymer, dict_transformations)

    polymer_counter = collections.Counter(current_polymer)
    print(polymer_counter)
    print(max(polymer_counter.values()) - min(polymer_counter.values()))


if __name__ == "__main__":
    main()

