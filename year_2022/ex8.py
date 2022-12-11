import collections
from dataclasses import dataclass
from typing import Dict, Set, List, Union, Optional, Callable

from common_helpers.position import Position, Direction


class Tree:
    is_visible_from_right: bool
    is_visible_from_top: bool
    is_visible_from_left: bool
    is_visible_from_bottom: bool
    height: int

    def __init__(self, height: str):
        self.is_visible_from_left = True
        self.is_visible_from_right = True
        self.is_visible_from_top = True
        self.is_visible_from_bottom = True
        self.height = int(height)

    def is_visible(self):
        return self.is_visible_from_right or \
               self.is_visible_from_left or \
               self.is_visible_from_bottom or \
               self.is_visible_from_top


def compute_scenic_score_given_tree(dict_trees: Dict[Position, Tree], tree_pos: Position):
    return get_len_view_direction(dict_trees, tree_pos, Direction.LEFT) \
           * get_len_view_direction(dict_trees, tree_pos, Direction.RIGHT) \
           * get_len_view_direction(dict_trees, tree_pos, Direction.UP) \
           * get_len_view_direction(dict_trees, tree_pos, Direction.DOWN)


def get_len_view_direction(dict_trees: Dict[Position, Tree], tree_pos: Position, direction: Direction) -> int:
    tree_height = dict_trees[tree_pos].height

    acc = 0
    new_pos = tree_pos
    while True:
        new_pos = new_pos.get_pos_direction(direction)
        try:
            candidate_height = dict_trees[new_pos].height
            if candidate_height < tree_height:
                acc += 1
            else:
                return acc + 1
        except KeyError:
            return acc


def main():
    with open("data.txt") as f:
        content = f.read().splitlines()

    dict_trees: Dict[Position, Tree] = {}

    max_y = len(content)
    max_x = len(content[0])

    for pos_y, line in enumerate(content):
        for pos_x, height_str in enumerate(line):
            dict_trees[Position(pos_x, pos_y)] = Tree(height_str)

    # left
    for y in range(max_y):
        max_height_found = -1
        for x in range(max_x):
            considered_tree = dict_trees[Position(x, y)]
            if considered_tree.height > max_height_found:
                max_height_found = considered_tree.height
            else:
                considered_tree.is_visible_from_left = False

    # right
    for y in range(max_y):
        max_height_found = -1
        for x in range(max_x - 1, -1, -1):
            considered_tree = dict_trees[Position(x, y)]
            if considered_tree.height > max_height_found:
                max_height_found = considered_tree.height
            else:
                considered_tree.is_visible_from_right = False

    # top
    for x in range(max_x):
        max_height_found = -1
        for y in range(max_y):
            considered_tree = dict_trees[Position(x, y)]
            if considered_tree.height > max_height_found:
                max_height_found = considered_tree.height
            else:
                considered_tree.is_visible_from_top = False

    # bottom
    for x in range(max_x):
        max_height_found = -1
        for y in range(max_y - 1, -1, -1):
            considered_tree = dict_trees[Position(x, y)]
            if considered_tree.height > max_height_found:
                max_height_found = considered_tree.height
            else:
                considered_tree.is_visible_from_bottom = False

    # print(dict_trees)
    acc = 0
    for pos, tree in dict_trees.items():
        if tree.is_visible():
            acc += 1

    # 1749 too low
    # part 1
    print(acc)

    # part 2
    min_score = 0
    for tree_pos in dict_trees.keys():
        candidate = compute_scenic_score_given_tree(dict_trees, tree_pos)
        if candidate > min_score:
            min_score = candidate

    print(min_score)


if __name__ == "__main__":
    main()
