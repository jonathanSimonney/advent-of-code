import copy


def compute_waiting_time_for_bus(min_time, bus_id):
    return bus_id - (min_time % bus_id)


with open("data.txt") as f:
    list_data = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line

first_timestamp_available = int(list_data[0])
list_buses_id = [int(x) if x != 'x' else None for x in list_data[1].split(",")]

first_bus_takable_id = None
min_time_departure = None

list_buses_offset = []

for needed_offset, id_bus in enumerate(list_buses_id):
    if id_bus is not None:
        list_buses_offset.append({"id": id_bus, "offset": needed_offset})

tested_departure_time = -1
loop_path = 1
while True:
    is_result_right = True
    tested_departure_time += loop_path
    iterated_list_buses = copy.deepcopy(list_buses_offset)
    nb_deleted_elem_in_iter = 0

    for idx, buses_info in enumerate(iterated_list_buses):
        time_since_last_departure = (tested_departure_time + buses_info["offset"]) % buses_info["id"]
        if time_since_last_departure != 0:
            is_result_right = False
        else:
            loop_path *= buses_info["id"]
            del list_buses_offset[idx - nb_deleted_elem_in_iter]
            nb_deleted_elem_in_iter += 1
    if is_result_right:
        break

# 537002774500 too low
print(tested_departure_time)
