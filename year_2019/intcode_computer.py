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

    def run_intcode_program(self, first_instruction=None, second_instruction=None):
        instruction_pointer = 0
        original_memory = self.memory.copy()
        if first_instruction is not None:
            self.memory[1] = first_instruction
        if second_instruction is not None:
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
        opcode_instruction = self.memory[instruction_pointer]

        opcode = int(str(opcode_instruction)[-2:])
        params_str = str(opcode_instruction)[:-2]

        if opcode == 99:
            return -1

        first_param_value = self.memory[instruction_pointer + 1]

        if opcode == 1:
            second_param_value = self.memory[instruction_pointer + 2]
            third_param_value = self.memory[instruction_pointer + 3]

            self.memory[third_param_value] = self._get_value_based_on_mode(first_param_value, params_str, 1) \
                                             + self._get_value_based_on_mode(second_param_value, params_str, 2)
            return 4

        if opcode == 2:
            second_param_value = self.memory[instruction_pointer + 2]
            third_param_value = self.memory[instruction_pointer + 3]

            self.memory[third_param_value] = self._get_value_based_on_mode(first_param_value, params_str, 1) \
                                             * self._get_value_based_on_mode(second_param_value, params_str, 2)
            return 4

        if opcode == 3:
            val_to_store = self.get_input_instruction()
            self.memory[first_param_value] = val_to_store
            return 2

        if opcode == 4:
            self.send_output_instruction(self._get_value_based_on_mode(first_param_value, params_str, 1))
            return 2

        raise AttributeError(
            "the opcode found at index " + instruction_pointer + ", " + str(opcode) + " isn't a valid opcode")

    def _get_value_based_on_mode(self, param_value, parameters_str, index_param):
        try:
            mode = int(parameters_str[-index_param])
        except IndexError:
            mode = 0
        if mode == 0:
            return self.memory[param_value]
        if mode == 1:
            return param_value

        raise AttributeError("unrecognised parameter mode, ", str(mode))
