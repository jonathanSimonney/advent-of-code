with open("data.txt") as f:
    content = [int(i) for i in f.readlines()]

set_results_reached = set()

acc = 0
idx = 0
while True:
    acc += content[idx]
    idx += 1
    if acc in set_results_reached:
        print(acc)
        break
    set_results_reached.add(acc)
    if idx == len(content):
        idx = 0
print(sum(content))
