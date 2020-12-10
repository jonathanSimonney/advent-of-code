import itertools
from year_2019.intcode_computer import IntcodeComputer


def make_a_getter_input(array_inputs_to_send_back):
    nb_time_method_called = 0

    def method_to_return():
        nonlocal nb_time_method_called
        val_to_return = array_inputs_to_send_back[nb_time_method_called]
        nb_time_method_called += 1
        return val_to_return
    return method_to_return


def make_handler_output_writing_to_list(list_to_write_to):

    def handle_output(value):
        nonlocal list_to_write_to
        list_to_write_to.append(value)

    return handle_output


def compute_phase_settings_result(intcode_computer_to_boot, list_phases):
    list_output = [0]
    output_handler = make_handler_output_writing_to_list(list_output)
    for index, phase_setting in enumerate(list_phases):
        singular_getter = make_a_getter_input([phase_setting, list_output[index]])
        intcode_computer_to_boot.run_intcode_program_from_start(get_input_instruction=singular_getter, send_output_instruction=output_handler)

    return list_output[-1]


def create_amplifier_computer_in_feedback_loop(intcode_computer_program, list_to_take_input_from):
    input_getter = make_a_getter_input(list_to_take_input_from)

    return {
        "computer": IntcodeComputer(intcode_computer_program, get_input_instruction=input_getter),
        "input_list": list_to_take_input_from,
    }


def compute_phase_settings_result_feedback_mode(intcode_computer_program, list_phases):
    list_computers = [create_amplifier_computer_in_feedback_loop(intcode_computer_program, [phase_settings]) for phase_settings in list_phases]

    list_computers[0]["input_list"].append(0)

    for index, computer in enumerate(list_computers):
        computer["output_list"] = list_computers[(index + 1) % len(list_computers)]["input_list"]
        output_list_handler = make_handler_output_writing_to_list(computer["output_list"])
        computer["computer"].send_output_instruction = output_list_handler

    final_value = 0
    while final_value == 0:
        for index, computer in enumerate(list_computers):
            try:
                computer["computer"].continue_intcode_program()
                if index == len(list_computers) - 1:
                    final_value = computer["output_list"][-1]
            except IndexError:
                continue

    return final_value


with open("data.txt") as f:
    content = f.readlines()


# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x) for x in content[0].strip().split(",")]
print(content)

intcode_computer = IntcodeComputer(content)

possible_settings_list = itertools.permutations([9, 8, 7, 6, 5])

# print(compute_phase_settings_result_feedback_mode(content, [9,8,7,6,5]))

list_possible_powers = []

for list_settings in possible_settings_list:
    list_possible_powers.append(compute_phase_settings_result_feedback_mode(content, list_settings))
print(max(list_possible_powers))
