from common_helpers.position import Position


def fold_along_x_axis(set_point_to_fold: set[Position], x_axis_pos: int):
    for point in set_point_to_fold.copy():
        if point.x > x_axis_pos:
            new_point_x = x_axis_pos - (point.x - x_axis_pos)
            set_point_to_fold.add(Position(new_point_x, point.y))
            set_point_to_fold.remove(point)


def fold_along_y_axis(set_point_to_fold: set[Position], y_axis_pos: int):
    for point in set_point_to_fold:
        if point.y > y_axis_pos:
            new_point_y = y_axis_pos - (point.y - y_axis_pos)
            set_point_to_fold.add(Position(point.x, new_point_y))
            set_point_to_fold.remove(point)


def main():
    with open("data.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [line.strip() for line in content]

    set_point_pos: set[Position] = set()

    list_folding = []

    for line in content:
        if line == '':
            continue
        elif ',' in line:
            line_splitted = line.split(',')
            set_point_pos.add(Position(int(line_splitted[0]), int(line_splitted[1])))
        else:
            line_splitted = line.split(' ')

            list_folding.append(line_splitted[-1].split('='))

    fold_along_x_axis(set_point_pos, int(list_folding[0][1]))
    print(len(set_point_pos))


if __name__ == "__main__":
    main()

