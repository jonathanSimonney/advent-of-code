from typing import TypedDict


class HexParsedDict(TypedDict):
    version: int
    type_id: int
    value: int
    sub_packets: list[dict]
    packet_bits_len: int


def convert_char_to_bin_data(char: str) -> str:
    dict_convert = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111',
    }

    return dict_convert[char]


def parse_bin_str_to_int(str_to_parse: str) -> int:
    return int(str_to_parse, 2)


def parse_number_hex_str(str_to_parse: str) -> [int]:
    reached_last_packet = False

    acc_str_num = ''
    idx_start = 0
    while not reached_last_packet:
        bits_to_look_in_current_iter = str_to_parse[idx_start:idx_start + 5]
        if bits_to_look_in_current_iter[0] == '0':
            reached_last_packet = True
        acc_str_num += bits_to_look_in_current_iter[1:]
        idx_start += 5

    if len(acc_str_num) % 4 != 0:
        print("weird")
    return [parse_bin_str_to_int(acc_str_num), idx_start]


def parse_operation_hex_str_counting_packets(str_to_parse: str) -> list[HexParsedDict]:
    list_parsed_hex: list[HexParsedDict] = []

    nb_sub_packets = parse_bin_str_to_int(str_to_parse[:11])
    nb_parsed_packets = 0
    len_parsed_packets = 0
    while nb_parsed_packets < nb_sub_packets:
        new_dict = parse_hex_str(str_to_parse[11 + len_parsed_packets:])
        list_parsed_hex.append(new_dict)
        nb_parsed_packets += 1
        len_parsed_packets += new_dict['packet_bits_len']

    return list_parsed_hex


def parse_operation_hex_str_counting_bits(str_to_parse: str) -> list[HexParsedDict]:
    list_parsed_hex: list[HexParsedDict] = []

    nb_bits_sub_packets = parse_bin_str_to_int(str_to_parse[:15])

    nb_parsed_bits = 0
    while nb_parsed_bits < nb_bits_sub_packets:
        new_dict = parse_hex_str(str_to_parse[15 + nb_parsed_bits:])
        list_parsed_hex.append(new_dict)
        nb_parsed_bits += new_dict['packet_bits_len']

    return list_parsed_hex


def parse_hex_str(str_to_parse: str) -> HexParsedDict:
    packet_version = parse_bin_str_to_int(str_to_parse[:3])
    packet_type_id = parse_bin_str_to_int(str_to_parse[3:6])

    value = 0
    sub_packets = []

    if packet_type_id == 4:
        [value, len_number_str] = parse_number_hex_str(str_to_parse[6:])
        packet_len = len_number_str + 6
    else:
        if str_to_parse[6] == '0':
            sub_packets = parse_operation_hex_str_counting_bits(str_to_parse[7:])
            int_sub_packets_additional_len = 15
        else:
            sub_packets = parse_operation_hex_str_counting_packets(str_to_parse[7:])
            int_sub_packets_additional_len = 11

        packet_len = \
            sum([singular_sub_packet['packet_bits_len'] for singular_sub_packet in sub_packets]) \
            + 7 \
            + int_sub_packets_additional_len

    return {
        'version': packet_version,
        'type_id': packet_type_id,
        'value': value,
        'sub_packets': sub_packets,
        'packet_bits_len': packet_len
    }


def rec_compute_sum_version(parsed_dict: HexParsedDict) -> int:
    sum_version = 0
    sum_version += parsed_dict['version']
    for packet in parsed_dict['sub_packets']:
        sum_version += rec_compute_sum_version(packet)

    return sum_version


def apply_mult_to_sub_packets(parsed_dicts_list: list[HexParsedDict]) -> int:
    acc = 1
    for parsed_dict in parsed_dicts_list:
        acc *= rec_compute_packet_value(parsed_dict)
    return acc


def rec_compute_packet_value(parsed_dict: HexParsedDict) -> int:
    if parsed_dict['type_id'] == 4:
        return parsed_dict['value']
    elif parsed_dict['type_id'] == 0:
        return sum([rec_compute_packet_value(singular_sub_packet) for singular_sub_packet in parsed_dict['sub_packets']])
    elif parsed_dict['type_id'] == 1:
        return apply_mult_to_sub_packets(parsed_dict['sub_packets'])
    elif parsed_dict['type_id'] == 2:
        return min([rec_compute_packet_value(singular_sub_packet) for singular_sub_packet in parsed_dict['sub_packets']])
    elif parsed_dict['type_id'] == 3:
        return max([rec_compute_packet_value(singular_sub_packet) for singular_sub_packet in parsed_dict['sub_packets']])
    elif parsed_dict['type_id'] == 5:
        return 1 if rec_compute_packet_value(parsed_dict['sub_packets'][0]) > rec_compute_packet_value(parsed_dict['sub_packets'][1]) else 0
    elif parsed_dict['type_id'] == 6:
        return 1 if rec_compute_packet_value(parsed_dict['sub_packets'][0]) < rec_compute_packet_value(parsed_dict['sub_packets'][1]) else 0
    elif parsed_dict['type_id'] == 7:
        return 1 if rec_compute_packet_value(parsed_dict['sub_packets'][0]) == rec_compute_packet_value(parsed_dict['sub_packets'][1]) else 0


def main():
    with open("data.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [line.strip() for line in content][0]
    hex_str = ''.join([convert_char_to_bin_data(char) for char in content])

    # print(parse_hex_str('11101110000000001101010000001100100000100011000001100000'))
    print(parse_hex_str(hex_str))
    print(parse_hex_str(hex_str)['packet_bits_len'])
    print(len(hex_str))
    print(rec_compute_sum_version(parse_hex_str(hex_str)))
    print(rec_compute_packet_value(parse_hex_str(hex_str)))


if __name__ == "__main__":
    main()
