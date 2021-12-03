with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x.strip()) for x in content]

acc = 0
for index in range(len(content) - 3):
    if content[index + 3] > content[index]:
        acc += 1

# 1682 too low
print(acc)
