import collections


def apply_one_day_to_lanterfish_dict(param_lanterfish_dict: dict):
    new_dict = collections.defaultdict(lambda: 0)

    for nb_day, nb_lanterfish in param_lanterfish_dict.items():
        if nb_day == 0:
            new_dict[8] += nb_lanterfish
            new_dict[6] += nb_lanterfish
        else:
            new_dict[nb_day - 1] += nb_lanterfish

    return new_dict


with open("data.txt") as f:
    content = f.readlines()[0].split(',')
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x) for x in content]

dict_content = collections.defaultdict(lambda: 0)
for lanterfish_time in content:
    dict_content[lanterfish_time] += 1

for _ in range(256):
    dict_content = apply_one_day_to_lanterfish_dict(dict_content)

print(sum([x for x in dict_content.values()]))
