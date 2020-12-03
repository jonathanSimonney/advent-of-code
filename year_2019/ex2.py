from year_2019.intcode_computer import IntcodeComputer

with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [int(x) for x in content[0].strip().split(",")]

intcode_computer = IntcodeComputer(content)

for noun in range(99):
    for verb in range(99):
        result = intcode_computer.run_intcode_program(noun, verb)
        if result == 19690720:
            print(noun, verb)
            break

