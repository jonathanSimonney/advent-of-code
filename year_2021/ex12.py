import collections
from copy import deepcopy


def add_line_conn_do_dict(line_to_parse: str, dict_to_fill: dict) -> None:
    line_as_list = line_to_parse.split('-')
    dict_to_fill[line_as_list[0]].append(line_as_list[1])
    dict_to_fill[line_as_list[1]].append(line_as_list[0])


def recursively_find_all_valid_path(
        dict_connections: dict,
        starting_path: list[str],
        set_forbidden_caves: set[str] = None
) -> list[list[str]]:

    if set_forbidden_caves is None:
        set_forbidden_caves = set()
    else:
        set_forbidden_caves = deepcopy(set_forbidden_caves)

    start_pos = starting_path[-1]

    if start_pos.islower():
        set_forbidden_caves.add(start_pos)

    acc_list = []

    current_iteration_considered_paths: list[list[str]] = []

    for cav_to_visit in dict_connections[start_pos]:
        if cav_to_visit == 'end':
            acc_list.append(starting_path + [cav_to_visit])
        elif cav_to_visit not in set_forbidden_caves:
            current_iteration_considered_paths.append(starting_path + [cav_to_visit])
    for current_iter_path in current_iteration_considered_paths:
        acc_list.extend(recursively_find_all_valid_path(dict_connections, current_iter_path, set_forbidden_caves))

    return acc_list


def main():
    with open("data.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [line.strip() for line in content]

    dict_connections: dict = collections.defaultdict(lambda: [])
    for line in content:
        add_line_conn_do_dict(line, dict_connections)

    list_paths = recursively_find_all_valid_path(dict_connections, ['start'])
    print(len(list_paths))


if __name__ == "__main__":
    main()

