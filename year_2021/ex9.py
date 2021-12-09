from common_helpers.position import Position

with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [[int(char) for char in line.strip()] for line in content]

dict_positions: dict = {}

for x, line in enumerate(content):
    for y, height in enumerate(line):
        dict_positions[Position(x, y)] = height

sum_risk_level = 0
for x, line in enumerate(content):
    for y, height in enumerate(line):
        pos_to_check = Position(x, y)
        pos_to_right = pos_to_check.get_right_pos()
        pos_to_left = pos_to_check.get_left_pos()
        pos_to_top = pos_to_check.get_top_pos()
        pos_to_bottom = pos_to_check.get_bottom_pos()
        if (pos_to_right not in dict_positions or dict_positions[pos_to_right] > height) \
                and (pos_to_left not in dict_positions or dict_positions[pos_to_left] > height) \
                and (pos_to_top not in dict_positions or dict_positions[pos_to_top] > height) \
                and (pos_to_bottom not in dict_positions or dict_positions[pos_to_bottom] > height):
            sum_risk_level += height + 1

print(sum_risk_level)