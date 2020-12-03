def generic_create_segment(x1, x2, y1, y2, dict_to_fill, distance_walked, origin):
    if x1 == x2:
        if y1 < y2:
            dict_to_fill["vertical"].append({"x": x1, "min_y": y1, "max_y": y2, "distance_walked": distance_walked, "origin": origin})
        else:
            dict_to_fill["vertical"].append({"x": x1, "min_y": y2, "max_y": y1, "distance_walked": distance_walked, "origin": origin})
    else:
        if x1 < x2:
            dict_to_fill["horizontal"].append({"y": y1, "min_x": x1, "max_x": x2, "distance_walked": distance_walked, "origin": origin})
        else:
            dict_to_fill["horizontal"].append({"y": y1, "min_x": x2, "max_x": x1, "distance_walked": distance_walked, "origin": origin})


def parse_wire(wire_string):
    dict_to_ret = {"horizontal": [], "vertical": []}
    x_coord = 0
    y_coord = 0
    distance_walked = 0

    wire_array = wire_string.split(",")
    for direction_indication in wire_array:
        elder_x_coord = x_coord
        elder_y_coord = y_coord

        vector_dir = direction_indication[0]
        vector_len = int(direction_indication[1:])

        if vector_dir == "R":
            x_coord += vector_len
            origin = elder_x_coord
        elif vector_dir == "L":
            x_coord -= vector_len
            origin = elder_x_coord
        elif vector_dir == "U":
            y_coord += vector_len
            origin = elder_y_coord
        elif vector_dir == "D":
            y_coord -= vector_len
            origin = elder_y_coord
        else:
            raise AttributeError("invalid vector_dir", vector_dir)

        generic_create_segment(elder_x_coord, x_coord, elder_y_coord, y_coord, dict_to_ret, distance_walked, origin)

        distance_walked += vector_len

    return dict_to_ret


def do_segment_intersect(horizontal, vertical):
    return vertical["min_y"] <= horizontal["y"] <= vertical["max_y"] and horizontal["min_x"] <= vertical["x"] <= horizontal["max_x"]


def compute_manhattan_dist(horizontal, vertical):
    return abs(horizontal["y"]) + abs(vertical["x"])


def compute_time_dist(horizontal, vertical):
    return horizontal["distance_walked"] + vertical["distance_walked"] + abs(horizontal["origin"] - vertical["x"]) + abs(horizontal["y"] - vertical["origin"])


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [parse_wire(x) for x in content]

min_time_dist = None

for horizontal_segment in content[0]["horizontal"]:
    for vertical_segment in content[1]["vertical"]:
        if do_segment_intersect(horizontal_segment, vertical_segment):
            candidate_dist = compute_time_dist(horizontal_segment, vertical_segment)
            if candidate_dist != 0 and (min_time_dist is None or min_time_dist > candidate_dist):
                min_time_dist = candidate_dist

for horizontal_segment in content[1]["horizontal"]:
    for vertical_segment in content[0]["vertical"]:
        if do_segment_intersect(horizontal_segment, vertical_segment):
            candidate_dist = compute_time_dist(horizontal_segment, vertical_segment)
            if candidate_dist != 0 and (min_time_dist is None or min_time_dist > candidate_dist):
                min_time_dist = candidate_dist

print(min_time_dist)

