import collections

with open("data.txt") as f:
    content = f.readlines()[0].split(',')
# you may also want to remove whitespace characters like `\n` at the end of each line
content = sorted(int(x) for x in content)

dict_content = collections.defaultdict(lambda: 0)
for horizontal_pos in content:
    dict_content[horizontal_pos] += 1
print(dict_content)

dict_alignment_cost: dict = {}

previous_iteration_key = None
for key in dict_content.keys():
    if key == 0:
        dict_alignment_cost[key] = sum(content)
    else:
        # find the alignment costr for next value thanks to previous value
        dict_alignment_cost[key] = dict_alignment_cost[previous_iteration_key] + (dict_content[previous_iteration_key] - )
    previous_iteration_key = key

print(min(dict_alignment_cost.values()))
