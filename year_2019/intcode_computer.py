def _run_intcode_instruction(program_memory, instruction_pointer):
    opcode = program_memory[instruction_pointer]
    if opcode == 99:
        return -1

    index_first_value = program_memory[instruction_pointer + 1]
    index_second_value = program_memory[instruction_pointer + 2]
    index_to_replace = program_memory[instruction_pointer + 3]
    if opcode == 1:
        program_memory[index_to_replace] = program_memory[index_first_value] + program_memory[index_second_value]
        return 4

    if opcode == 2:
        program_memory[index_to_replace] = program_memory[index_first_value] * program_memory[index_second_value]
        return 4

    raise AttributeError(
        "the opcode found at index " + instruction_pointer + ", " + opcode + " isn't a valid opcode")


class IntcodeComputer:
    memory = []
    instruction_pointer = 0

    def __init__(self, memory):
        self.memory = memory
        self.instruction_pointer = 0

    def run_intcode_program(self, first_instruction, second_instruction):
        instruction_pointer = 0
        local_memory_to_use = self.memory.copy()
        local_memory_to_use[1] = first_instruction
        local_memory_to_use[2] = second_instruction
        while True:
            instruction_pointer_increment = _run_intcode_instruction(local_memory_to_use, instruction_pointer)
            if instruction_pointer_increment == -1:
                break
            instruction_pointer += instruction_pointer_increment
        return local_memory_to_use[0]


