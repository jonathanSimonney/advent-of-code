def concat_in_order(point_1, point_2):
    return f"x{point_1['x']}y{point_1['y']} x{point_2['x']}y{point_2['y']}"


def compute_key_str_los(point_1, point_2):
    if point_1["x"] < point_2["x"]:
        return concat_in_order(point_1, point_2)
    if point_1["x"] > point_2["x"]:
        return concat_in_order(point_2, point_1)
    if point_1["y"] < point_2["y"]:
        return concat_in_order(point_1, point_2)
    if point_1["y"] > point_2["y"]:
        return concat_in_order(point_2, point_1)
    raise AttributeError("2 params have the same value")



with open("data.txt") as f:
    content = f.readlines()

list_asteroids_loc = []
print(content)
for x, line in enumerate(content):
    for y, char in enumerate(line):
        if char == "#":
            list_asteroids_loc.append({"x": x, "y": y})

print(list_asteroids_loc, len(list_asteroids_loc))

dict_nb_asteroids_seen = {}
for loc in list_asteroids_loc:
    ...

