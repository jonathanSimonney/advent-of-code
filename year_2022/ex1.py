from typing import List

with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
# content = [parse_line_content(x) for x in content]

acc: int = 0
list_cal_max: List[int] = []

for line in content:
    if line == "\n":
        if len(list_cal_max) < 3:
            list_cal_max.append(acc)
        elif min(list_cal_max) < acc:
            list_cal_max.remove(min(list_cal_max))
            list_cal_max.append(acc)
        acc = 0
    else:
        acc += int(line)

# 1682 too low
print(sum(list_cal_max))
