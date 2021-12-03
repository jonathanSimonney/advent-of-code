with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip().split(" ") for x in content]

depth = 0
pos = 0
aim = 0
for instruction in content:
    if instruction[0] == 'forward':
        pos += int(instruction[1])
        depth += int(instruction[1]) * aim
    elif instruction[0] == 'down':
        aim += int(instruction[1])
    elif instruction[0] == 'up':
        aim -= int(instruction[1])

# 1682 too low
print(depth * pos)
