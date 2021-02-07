import itertools
from year_2019.intcode_computer import IntcodeComputer


def get_input():
    return 2


def handle_output(value):
    print(value)


with open("data.txt") as f:
    content = f.readlines()


# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x) for x in content[0].strip().split(",")]
print(content)

intcode_computer = IntcodeComputer(content)

intcode_computer.run_intcode_program_from_start(get_input_instruction=get_input, send_output_instruction=handle_output)


