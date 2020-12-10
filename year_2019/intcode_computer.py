class IntcodeComputer:
    memory = []
    instruction_pointer = 0
    get_input_instruction = None
    send_output_instruction = None

    def __init__(self, memory, get_input_instruction=None, send_output_instruction=None):
        self.memory = memory.copy()
        self.instruction_pointer = 0
        self.get_input_instruction = get_input_instruction
        self.send_output_instruction = send_output_instruction

    def run_intcode_program_from_start(self, first_instruction=None, second_instruction=None, get_input_instruction=None, send_output_instruction=None):
        self.instruction_pointer = 0
        original_memory = self.memory.copy()
        if first_instruction is not None:
            self.memory[1] = first_instruction
        if second_instruction is not None:
            self.memory[2] = second_instruction
        if get_input_instruction is not None:
            self.get_input_instruction = get_input_instruction
        if send_output_instruction is not None:
            self.send_output_instruction = send_output_instruction
        while True:
            self._run_intcode_instruction()
            if self.instruction_pointer is None:
                break

        val_to_ret = self.memory[0]

        self.memory = original_memory
        return val_to_ret

    def continue_intcode_program(self):
        while True:
            self._run_intcode_instruction()
            if self.instruction_pointer is None:
                break

        return self.memory[0]

    def _run_intcode_instruction(self):
        opcode_instruction = self.memory[self.instruction_pointer]

        opcode = int(str(opcode_instruction)[-2:])
        params_str = str(opcode_instruction)[:-2]

        if opcode == 99:
            self.instruction_pointer = None
            return

        first_param_value = self.memory[self.instruction_pointer + 1]

        if opcode == 1:
            second_param_value = self.memory[self.instruction_pointer + 2]
            third_param_value = self.memory[self.instruction_pointer + 3]

            self.memory[third_param_value] = self._get_value_based_on_mode(first_param_value, params_str, 1) \
                                             + self._get_value_based_on_mode(second_param_value, params_str, 2)
            self.instruction_pointer += 4
            return

        if opcode == 2:
            second_param_value = self.memory[self.instruction_pointer + 2]
            third_param_value = self.memory[self.instruction_pointer + 3]

            self.memory[third_param_value] = self._get_value_based_on_mode(first_param_value, params_str, 1) \
                                             * self._get_value_based_on_mode(second_param_value, params_str, 2)
            self.instruction_pointer += 4
            return

        if opcode == 3:
            val_to_store = self.get_input_instruction()
            self.memory[first_param_value] = val_to_store
            self.instruction_pointer += 2
            return

        if opcode == 4:
            self.send_output_instruction(self._get_value_based_on_mode(first_param_value, params_str, 1))
            self.instruction_pointer += 2
            return

        if opcode == 5:
            first_param = self._get_value_based_on_mode(first_param_value, params_str, 1)
            if first_param != 0:
                second_param_value = self.memory[self.instruction_pointer + 2]
                self.instruction_pointer = self._get_value_based_on_mode(second_param_value, params_str, 2)
                return
            self.instruction_pointer += 3
            return

        if opcode == 6:
            first_param = self._get_value_based_on_mode(first_param_value, params_str, 1)
            if first_param == 0:
                second_param_value = self.memory[self.instruction_pointer + 2]
                self.instruction_pointer = self._get_value_based_on_mode(second_param_value, params_str, 2)
                return
            self.instruction_pointer += 3
            return

        if opcode == 7:
            second_param_value = self.memory[self.instruction_pointer + 2]
            third_param_value = self.memory[self.instruction_pointer + 3]

            first_param = self._get_value_based_on_mode(first_param_value, params_str, 1)
            second_param = self._get_value_based_on_mode(second_param_value, params_str, 2)
            if first_param < second_param:
                self.memory[third_param_value] = 1
            else:
                self.memory[third_param_value] = 0
            self.instruction_pointer += 4
            return

        if opcode == 8:
            second_param_value = self.memory[self.instruction_pointer + 2]
            third_param_value = self.memory[self.instruction_pointer + 3]

            first_param = self._get_value_based_on_mode(first_param_value, params_str, 1)
            second_param = self._get_value_based_on_mode(second_param_value, params_str, 2)
            if first_param == second_param:
                self.memory[third_param_value] = 1
            else:
                self.memory[third_param_value] = 0
            self.instruction_pointer += 4
            return

        raise AttributeError(
            "the opcode found at index " + str(self.instruction_pointer) + ", " + str(opcode) + " isn't a valid opcode")

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
