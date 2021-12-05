import collections
from dataclasses import dataclass

from common_helpers.position import Position


@dataclass(frozen=True)
class Vector:
    origin: Position
    to: Position


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

vector_list: list[Vector] = []
for line in content:
    split_line = line.split(' -> ')
    pos_1_as_list = split_line[0].split(',')
    pos_2_as_list = split_line[1].split(',')
    vector_list.append(
        Vector(
            Position(int(pos_1_as_list[0]), int(pos_1_as_list[1])),
            Position(int(pos_2_as_list[0]), int(pos_2_as_list[1]))
        )
    )

dict_positions_to_nb_currents = collections.defaultdict(lambda: 0)
for vector in vector_list:
    if vector.origin.x == vector.to.x:
        if vector.origin.y > vector.to.y:
            range_to_iterate = range(vector.to.y, vector.origin.y + 1)
        else:
            range_to_iterate = range(vector.origin.y, vector.to.y + 1)
        for coord_y in range_to_iterate:
            dict_positions_to_nb_currents[Position(vector.origin.x, coord_y)] += 1
    elif vector.origin.y == vector.to.y:
        if vector.origin.x > vector.to.x:
            range_to_iterate = range(vector.to.x, vector.origin.x + 1)
        else:
            range_to_iterate = range(vector.origin.x, vector.to.x + 1)
        for coord_x in range_to_iterate:
            dict_positions_to_nb_currents[Position(coord_x, vector.origin.y)] += 1
    else:
        if vector.origin.y > vector.to.y:
            y_path = -1
        else:
            y_path = 1
        if vector.origin.x > vector.to.x:
            x_path = -1
        else:
            x_path = 1

        coord_x = vector.origin.x
        coord_y = vector.origin.y
        for i in range(abs(vector.origin.y - vector.to.y) + 1):
            dict_positions_to_nb_currents[Position(coord_x, coord_y)] += 1
            coord_x += x_path
            coord_y += y_path

# 1208 too low
# 21029 too low for part 2
# 22049 too low for part 2
print(sum([1 for i in dict_positions_to_nb_currents.values() if i > 1]))
