import collections


with open("data.txt") as f:
    content = f.readlines()

nb_2_letters = 0
nb_3_letters = 0

for line in content:
    counter_line = collections.Counter(line)

    should_update_2_letters = False
    should_update_3_letters = False
    for count in counter_line.values():
        if count == 2:
            should_update_2_letters = True
        if count == 3:
            should_update_3_letters = True

    nb_2_letters += int(should_update_2_letters)
    nb_3_letters += int(should_update_3_letters)

print(nb_2_letters * nb_3_letters)


