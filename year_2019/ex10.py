import collections
import math
from enum import Enum
from functools import cmp_to_key


class Cadran(Enum):
    EXACT_UP = 0
    UP_RIGHT = 1
    EXACT_RIGHT = 2
    DOWN_RIGHT = 3
    EXACT_DOWN = 4
    DOWN_LEFT = 5
    EXACT_LEFT = 6
    UP_LEFT = 7


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


def compute_cadran_position(relative_x_pos, relative_y_pos):
    if relative_y_pos < 0:
        if relative_x_pos > 0:
            return Cadran.UP_RIGHT
        elif relative_x_pos < 0:
            return Cadran.UP_LEFT
        else:
            return Cadran.EXACT_UP
    elif relative_y_pos > 0:
        if relative_x_pos > 0:
            return Cadran.DOWN_RIGHT
        elif relative_x_pos < 0:
            return Cadran.DOWN_LEFT
        else:
            return Cadran.EXACT_DOWN
    else:
        if relative_x_pos > 0:
            return Cadran.EXACT_RIGHT
        elif relative_x_pos < 0:
            return Cadran.EXACT_LEFT


def generate_compare_pos_asteroids_from_origin(x_origin, y_origin):
    def compare_pos_asteroids(pos_1, pos_2):
        pos_1_relative_y = pos_1['y'] - y_origin
        pos_1_relative_x = pos_1['x'] - x_origin
        pos_2_relative_y = pos_2['y'] - y_origin
        pos_2_relative_x = pos_2['x'] - x_origin

        cadran_pos_1 = compute_cadran_position(pos_1_relative_x, pos_1_relative_y)
        cadran_pos_2 = compute_cadran_position(pos_2_relative_x, pos_2_relative_y)

        if cadran_pos_1 != cadran_pos_2:
            return cadran_pos_1.value - cadran_pos_2.value

        ratio_pos_1 = abs(pos_1_relative_x / pos_1_relative_y)
        ratio_pos_2 = abs(pos_2_relative_x / pos_2_relative_y)

        if cadran_pos_1 == Cadran.UP_RIGHT:
            return -1 if ratio_pos_1 < ratio_pos_2 else 1
        if cadran_pos_1 == Cadran.DOWN_RIGHT:
            return 1 if ratio_pos_1 < ratio_pos_2 else -1
        if cadran_pos_1 == Cadran.DOWN_LEFT:
            return -1 if ratio_pos_1 < ratio_pos_2 else 1
        if cadran_pos_1 == Cadran.UP_LEFT:
            return 1 if ratio_pos_1 < ratio_pos_2 else -1
    return compare_pos_asteroids

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

dict_nb_asteroids_seen = collections.defaultdict(lambda: {'nb': 0, 'locations': []})
for idx1, loc1 in enumerate(list_asteroids_loc):
    for loc2 in list_asteroids_loc[idx1 + 1:]:
        if has_los_between(loc1, loc2, set_pos_asteroids):
            dict_nb_asteroids_seen[compute_key(loc1)]['nb'] += 1
            dict_nb_asteroids_seen[compute_key(loc2)]['nb'] += 1
            dict_nb_asteroids_seen[compute_key(loc1)]['locations'].append(loc2)
            dict_nb_asteroids_seen[compute_key(loc2)]['locations'].append(loc1)

max_nb_asteroids = 0
loc_key = None
for key, nb_asteroids_dict in dict_nb_asteroids_seen.items():
    if nb_asteroids_dict['nb'] > max_nb_asteroids:
        max_nb_asteroids = nb_asteroids_dict['nb']
        loc_key = key

# 342 trop haut
print(max_nb_asteroids, loc_key)

x_pos = 22
y_pos = 25
print(
    sorted(
        dict_nb_asteroids_seen[loc_key]['locations'],
        key=cmp_to_key(generate_compare_pos_asteroids_from_origin(x_pos, y_pos))
    )[199]
)
