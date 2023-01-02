import re
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class ValveData:
    id: str
    flow_rate: int
    linked_valve_id: List[str]


def parse_line(str_param: str) -> ValveData:
    matched_elem = re.findall(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)", str_param)

    valve_id = matched_elem[0][0]
    valve_flow_rate = int(matched_elem[0][1])
    linked_valve_id_list = matched_elem[0][2].split(", ")

    return ValveData(valve_id, valve_flow_rate, linked_valve_id_list)


def main():
    with open("data.txt") as f:
        content = [parse_line(line) for line in f.read().splitlines()]

    print(content)
    dict_valve_id_to_flow_rate: Dict[str, int]


if __name__ == "__main__":
    main()
