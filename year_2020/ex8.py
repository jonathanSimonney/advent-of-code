import copy


def parse_line_content(str_line):
    array_line = str_line.split(" ")

    value_to_put = int(array_line[1][1:])
    if array_line[1][0] == "-":
        value_to_put = -value_to_put

    return {"instruction": array_line[0], "value": value_to_put, "first_execution": True}


def run_program(instructions):
    acc = 0
    pointer = 0
    ran_into_infinite_loop = False

    while True:
        try:
            instruction_to_exec = instructions[pointer]
        except IndexError:
            ran_into_infinite_loop = False
            break
        if not instruction_to_exec["first_execution"]:
            ran_into_infinite_loop = True
            break
        instruction_to_exec["first_execution"] = False

        command = instruction_to_exec["instruction"]
        if command == "nop":
            pointer += 1
            continue

        if command == "acc":
            acc += instruction_to_exec["value"]
            pointer += 1
            continue

        if command == "jmp":
            pointer += instruction_to_exec["value"]
            continue

    return {"has_infinite_loop": ran_into_infinite_loop, "acc": acc}


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line

array_instructions = [parse_line_content(x.strip()) for x in content]

for index, instruction in enumerate(array_instructions):
    copy_instructions = copy.deepcopy(array_instructions)
    if instruction["instruction"] == "jmp":
        copy_instructions[index]["instruction"] = "nop"
        program_result = run_program(copy_instructions)
        if not program_result["has_infinite_loop"]:
            break
    elif instruction["instruction"] == "nop":
        copy_instructions[index]["instruction"] = "jmp"
        program_result = run_program(copy_instructions)

        if not program_result["has_infinite_loop"]:
            break

# 16436 too low
# 36625 too high
print(program_result["acc"])
