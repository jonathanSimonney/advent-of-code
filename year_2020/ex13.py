def compute_waiting_time_for_bus(min_time, bus_id):
    return bus_id - (min_time % bus_id)


with open("data.txt") as f:
    list_data = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line

first_timestamp_available = int(list_data[0])
list_buses_id = [int(x) if x != 'x' else None for x in list_data[1].split(",")]

first_bus_takable_id = None
min_time_departure = None

for id_bus in list_buses_id:
    if id_bus is not None:
        waiting_time_candidate = compute_waiting_time_for_bus(first_timestamp_available, id_bus)
        if min_time_departure is None or waiting_time_candidate < min_time_departure:
            min_time_departure = waiting_time_candidate
            first_bus_takable_id = id_bus

print(first_bus_takable_id * min_time_departure)
