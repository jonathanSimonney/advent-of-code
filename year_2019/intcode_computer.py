class IntcodeComputer:
    memory = []
    instruction_pointer = 0
    get_input_instruction = None
    send_output_instruction = None

    def __init__(self, memory, get_input_instruction=None, send_output_instruction=None):
        self.memory = memory
        self.instruction_pointer = 0
        self.get_input_instruction = get_input_instruction
        self.send_output_instruction = send_output_instruction

    def run_intcode_program(self, first_instruction, second_instruction):
        instruction_pointer = 0
        original_memory = self.memory.copy()
        self.memory[1] = first_instruction
        self.memory[2] = second_instruction
        while True:
            instruction_pointer_increment = self._run_intcode_instruction(instruction_pointer)
            if instruction_pointer_increment == -1:
                break
            instruction_pointer += instruction_pointer_increment

        val_to_ret = self.memory[0]

        self.memory = original_memory
        return val_to_ret

    def _run_intcode_instruction(self, instruction_pointer):
        opcode = self.memory[instruction_pointer]
        if opcode == 99:
            return -1

        index_first_value = self.memory[instruction_pointer + 1]
        index_second_value = self.memory[instruction_pointer + 2]
        index_to_replace = self.memory[instruction_pointer + 3]
        if opcode == 1:
            self.memory[index_to_replace] = self.memory[index_first_value] + self.memory[index_second_value]
            return 4

        if opcode == 2:
            self.memory[index_to_replace] = self.memory[index_first_value] * self.memory[index_second_value]
            return 4

        if opcode == 3:
            val_to_store = self.get_input_instruction()
            self.memory[index_first_value] = val_to_store
            return 2

        if opcode == 4:
            self.send_output_instruction(self.memory[index_first_value])
            return 2

        raise AttributeError(
            "the opcode found at index " + instruction_pointer + ", " + opcode + " isn't a valid opcode")

    # todo def a _get_value_based_on_mode(), taking a parameter and a mode, and based on mode, getting it in memory or at the opposite, getting it directly


