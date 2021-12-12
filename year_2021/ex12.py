import collections
from copy import deepcopy


def add_line_conn_do_dict(line_to_parse: str, dict_to_fill: dict) -> None:
    line_as_list = line_to_parse.split('-')
    dict_to_fill[line_as_list[0]].append(line_as_list[1])
    dict_to_fill[line_as_list[1]].append(line_as_list[0])


def recursively_find_all_valid_path(
        dict_connections: dict,
        starting_path: list[str],
        set_forbidden_caves: set[str] = None,
        has_already_used_double_visit: bool = False
) -> list[list[str]]:

    if set_forbidden_caves is None:
        set_forbidden_caves = set()
    else:
        set_forbidden_caves = deepcopy(set_forbidden_caves)

    start_pos = starting_path[-1]

    if start_pos.islower():
        set_forbidden_caves.add(start_pos)

    acc_list = []

    for cav_to_visit in dict_connections[start_pos]:
        if cav_to_visit == 'end':
            acc_list.append(starting_path + [cav_to_visit])
        elif cav_to_visit not in set_forbidden_caves:
            acc_list.extend(recursively_find_all_valid_path(
                dict_connections,
                starting_path + [cav_to_visit],
                set_forbidden_caves,
                has_already_used_double_visit
            ))
        elif (cav_to_visit in set_forbidden_caves) and (cav_to_visit != 'start') and (not has_already_used_double_visit):
            acc_list.extend(recursively_find_all_valid_path(
                dict_connections,
                starting_path + [cav_to_visit],
                set_forbidden_caves,
                True
            ))

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

