from common_helpers.position import Position


class Board:
    _lines: list[[str]]
    _marked_numbers: [str]
    _dict_num_unmarked: dict

    def __init__(self, line_array: list[[str]]):
        self._lines = line_array
        self._marked_numbers = []
        self._dict_num_unmarked = {}
        for x, line in enumerate(line_array):
            for y, num in enumerate(line):
                self._dict_num_unmarked[num] = Position(x, y)

    def draw_number(self, number_drawn: str) -> bool:
        self._marked_numbers.append(number_drawn)
        if number_drawn not in self._dict_num_unmarked:
            return False
        position_drawn: Position = self._dict_num_unmarked[number_drawn]
        del self._dict_num_unmarked[number_drawn]
        return self._check_victory_on_pos(position_drawn)

    def compute_score(self) -> int:
        return sum([int(x) for x in self._dict_num_unmarked.keys()]) * int(self._marked_numbers[-1])

    def _check_victory_on_pos(self, pos_to_check: Position) -> bool:
        return self._check_victory_on_x_axis(pos_to_check.x) or \
               self._check_victory_on_y_axis(pos_to_check.y)

    def _check_victory_on_x_axis(self, x_coord_to_check: int) -> bool:
        for coord in self._dict_num_unmarked.values():
            if coord.x == x_coord_to_check:
                return False

        return True

    def _check_victory_on_y_axis(self, y_coord_to_check: int) -> bool:
        for coord in self._dict_num_unmarked.values():
            if coord.y == y_coord_to_check:
                return False

        return True


def get_winning_board(list_candidates_board: [Board], list_number_to_draw: [str]):
    for nb_drawn in list_number_to_draw:
        for board in list_candidates_board:
            if board.draw_number(nb_drawn):
                return board


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

nb_drawns: [str] = content[0].split(",")

list_board: [Board] = []
lines: list[[str]] = []
for line in content[2:]:
    if line == '':
        list_board.append(Board(lines))
        lines = []
    else:
        lines.append(line.split())
list_board.append(Board(lines))


# 38550 too low
print(get_winning_board(list_board, nb_drawns).compute_score())
