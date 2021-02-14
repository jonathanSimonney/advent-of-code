with open("data.txt") as f:
    content = f.readlines()

list_asteroids_loc = []
print(content)
for x, line in enumerate(content):
    for y, char in enumerate(line):
        if char == "#":
            list_asteroids_loc.append((x, y))

print(list_asteroids_loc, len(list_asteroids_loc))

dict_nb_asteroids_seen = {}
for loc in list_asteroids_loc:
    ...

