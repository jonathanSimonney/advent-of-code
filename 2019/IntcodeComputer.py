class IntcodeComputer:
    memory = []
    instruction_pointer = 0

    def run_program(self, first_instruction, second_instruction):
        ...

    def _run_intcode_instruction(self, program_memory, instruction_pointer):
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

    def run_intcode_program(self, program_memory, first_instruction, second_instruction):
        instruction_pointer = 0
        program_memory[1] = first_instruction
        program_memory[2] = second_instruction
        while True:
            instruction_pointer_increment = self._run_intcode_instruction(program_memory, instruction_pointer)
            if instruction_pointer_increment == -1:
                break
            instruction_pointer += instruction_pointer_increment
        return program_memory[0]

