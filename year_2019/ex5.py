from year_2019.intcode_computer import IntcodeComputer


def get_input():
    return 1


def handle_output(value):
    print(value)


with open("data.txt") as f:
    content = f.readlines()

print(content)

# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x) for x in content[0].strip().split(",")]

intcode_computer = IntcodeComputer(content, get_input, handle_output)

intcode_computer.run_intcode_program()

