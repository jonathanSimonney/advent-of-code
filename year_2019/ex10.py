import collections
import math


def compute_key_with_coords(x_coord, y_coord):
    return f"x{x_coord}y{y_coord}"


def compute_key(point):
    return compute_key_with_coords(point['x'], point['y'])


def has_los_between(point_1, point_2, set_pos_asteroids_to_check):
    if point_1['x'] == point_2['x']:
        for y_pos in range(point_1['y'] + 1, point_2['y']):
            if compute_key_with_coords(point_1['x'], y_pos) in set_pos_asteroids_to_check:
                return False
        return True

    if point_1['y'] == point_2['y']:
        for x_pos in range(point_1['x'] + 1, point_2['x']):
            if compute_key_with_coords(x_pos, point_1['y']) in set_pos_asteroids_to_check:
                return False
        return True

    diff_y = point_2['y'] - point_1['y']
    diff_x = point_2['x'] - point_1['x']
    dividor = math.gcd(diff_x, diff_y)

    path_x = int(diff_x / dividor)
    path_y = int(diff_y / dividor)

    for i in range(1, dividor):
        if compute_key_with_coords(point_1['x'] + path_x * i, point_1['y'] + path_y * i) in set_pos_asteroids_to_check:
            return False

    return True


with open("data.txt") as f:
    content = f.readlines()

list_asteroids_loc = []
print(content)
for y, line in enumerate(content):
    for x, char in enumerate(line):
        if char == "#":
            list_asteroids_loc.append({"x": x, "y": y})

print(list_asteroids_loc, len(list_asteroids_loc))

set_pos_asteroids = set()
for loc in list_asteroids_loc:
    set_pos_asteroids.add(compute_key(loc))

dict_nb_asteroids_seen = collections.defaultdict(lambda: 0)
for idx1, loc1 in enumerate(list_asteroids_loc):
    for loc2 in list_asteroids_loc[idx1 + 1:]:
        if has_los_between(loc1, loc2, set_pos_asteroids):
            dict_nb_asteroids_seen[compute_key(loc1)] += 1
            dict_nb_asteroids_seen[compute_key(loc2)] += 1

max_nb_asteroids = 0
loc_key = None
for key, nb_asteroids in dict_nb_asteroids_seen.items():
    if nb_asteroids > max_nb_asteroids:
        max_nb_asteroids = nb_asteroids
        loc_key = key

# 342 trop haut
print(max_nb_asteroids, loc_key)
