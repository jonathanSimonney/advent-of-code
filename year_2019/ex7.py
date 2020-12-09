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
        intcode_computer_to_boot.run_intcode_program(get_input_instruction=singular_getter, send_output_instruction=output_handler)

    return list_output[-1]


with open("testData.txt") as f:
    content = f.readlines()


# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x) for x in content[0].strip().split(",")]
print(content)

intcode_computer = IntcodeComputer(content)

print(compute_phase_settings_result(intcode_computer, [4, 3, 2, 1, 0]))
