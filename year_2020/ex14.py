def parse_mask_to_dict(mask_str):
    dict_to_return = {}

    for idx, char in enumerate(mask_str):
        if char != 'X':
            dict_to_return[idx] = char

    return dict_to_return


def write_value_in_mem_with_mask(adress_to_write, value_memory, mask_to_apply, memory_dict):
    value_as_36_bits_array = list(format(value_memory, '036b'))
    for idx, value in mask_to_apply.items():
        value_as_36_bits_array[idx] = value

    memory_dict[adress_to_write] = "".join(value_as_36_bits_array)


def write_value_in_mem_with_mask_v2(adress_to_write, value_memory, mask_to_apply, memory_dict):
    value_as_36_bits_array = format(value_memory, '036b')
    adress_as_36_bits_array = list(format(adress_to_write, '036b'))
    list_adresses_to_write = [""]

    for idx, value in enumerate(mask_to_apply):
        list_adresses_to_iterate = list_adresses_to_write.copy()
        if value == "0":
            for address_idx, address in enumerate(list_adresses_to_iterate):
                list_adresses_to_write[address_idx] += adress_as_36_bits_array[idx]
        elif value == "1":
            for address_idx, address in enumerate(list_adresses_to_iterate):
                list_adresses_to_write[address_idx] += "1"
        elif value == "X":
            for address_idx, address in enumerate(list_adresses_to_iterate):
                # print("appending an address")
                list_adresses_to_write[address_idx] += "0"
                list_adresses_to_write.append(address + "1")

    for address_as_str in list_adresses_to_write:
        memory_dict[int(address_as_str, 2)] = "".join(value_as_36_bits_array)


with open("data.txt") as f:
    list_instruction = [x.strip() for x in f.readlines()]
# you may also want to remove whitespace characters like `\n` at the end of each line

mask = None
memory = {}

for instruction_str in list_instruction:
    if instruction_str[:4] == "mask":
        mask = instruction_str[7:]
    else:
        instruction_array = instruction_str.split(" = ")
        memory_adress_to_write = int(instruction_array[0].split("[")[1].replace("]", ""))
        value_to_write = int(instruction_array[1])
        # write_value_in_mem_with_mask(memory_adress_to_write, value_to_write, mask, memory)
        write_value_in_mem_with_mask_v2(memory_adress_to_write, value_to_write, mask, memory)

acc = 0
for elem in memory:
    acc += int(memory[elem], 2)

print(acc)
