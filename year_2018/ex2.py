import collections


# copypasted from https://stackoverflow.com/a/25216604/7059810
def match(s1, s2):
    ok = False

    for c1, c2 in zip(s1, s2):
        if c1 != c2:
            if ok:
                return False
            else:
                ok = True

    return ok


with open("data.txt") as f:
    content = f.readlines()

nb_2_letters = 0
nb_3_letters = 0

should_break = False
for idx, line in enumerate(content):
    if not should_break:
        for compared_line in content[idx + 1:]:
            if match(line, compared_line):
                print(f"match found! between {line} and {compared_line}")
                should_break = True
                break
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


