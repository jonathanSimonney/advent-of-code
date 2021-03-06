def parse_array_into_dict(array_to_parse):
    dict_to_return = {}
    for idx, value in enumerate(array_to_parse):
        dict_to_return[idx] = value
    return dict_to_return


class IntcodeComputer:
    memory = {}
    instruction_pointer = 0
    relative_base = 0
    get_input_instruction = None
    send_output_instruction = None

    def __init__(self, memory_array, get_input_instruction=None, send_output_instruction=None):
        self.memory = parse_array_into_dict(memory_array)
        self.instruction_pointer = 0
        self.relative_base = 0
        self.get_input_instruction = get_input_instruction
        self.send_output_instruction = send_output_instruction

    def run_intcode_program_from_start(self, first_instruction=None, second_instruction=None, get_input_instruction=None, send_output_instruction=None):
        self.instruction_pointer = 0
        self.relative_base = 0
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

        first_param_value = self._get_value_in_memory_fallback_0(self.instruction_pointer + 1)

        if opcode == 1:
            second_param_value = self._get_value_in_memory_fallback_0(self.instruction_pointer + 2)
            third_param_value = self._get_value_in_memory_fallback_0(self.instruction_pointer + 3)
            value_to_write = self._get_value_based_on_mode(first_param_value, params_str, 1) \
                                             + self._get_value_based_on_mode(second_param_value, params_str, 2)

            self._write_value_based_on_mode(third_param_value, params_str, 3, value_to_write)

            self.instruction_pointer += 4
            return

        if opcode == 2:
            second_param_value = self._get_value_in_memory_fallback_0(self.instruction_pointer + 2)
            third_param_value = self._get_value_in_memory_fallback_0(self.instruction_pointer + 3)

            value_to_write = self._get_value_based_on_mode(first_param_value, params_str, 1) \
                                             * self._get_value_based_on_mode(second_param_value, params_str, 2)

            self._write_value_based_on_mode(third_param_value, params_str, 3, value_to_write)

            self.instruction_pointer += 4
            return

        if opcode == 3:
            val_to_store = self.get_input_instruction()
            self._write_value_based_on_mode(first_param_value, params_str, 1, val_to_store)

            self.instruction_pointer += 2
            return

        if opcode == 4:
            self.send_output_instruction(self._get_value_based_on_mode(first_param_value, params_str, 1))
            self.instruction_pointer += 2
            return

        if opcode == 5:
            first_param = self._get_value_based_on_mode(first_param_value, params_str, 1)
            if first_param != 0:
                second_param_value = self._get_value_in_memory_fallback_0(self.instruction_pointer + 2)
                self.instruction_pointer = self._get_value_based_on_mode(second_param_value, params_str, 2)
                return
            self.instruction_pointer += 3
            return

        if opcode == 6:
            first_param = self._get_value_based_on_mode(first_param_value, params_str, 1)
            if first_param == 0:
                second_param_value = self._get_value_in_memory_fallback_0(self.instruction_pointer + 2)
                self.instruction_pointer = self._get_value_based_on_mode(second_param_value, params_str, 2)
                return
            self.instruction_pointer += 3
            return

        if opcode == 7:
            second_param_value = self._get_value_in_memory_fallback_0(self.instruction_pointer + 2)
            third_param_value = self._get_value_in_memory_fallback_0(self.instruction_pointer + 3)

            first_param = self._get_value_based_on_mode(first_param_value, params_str, 1)
            second_param = self._get_value_based_on_mode(second_param_value, params_str, 2)
            if first_param < second_param:
                self._write_value_based_on_mode(third_param_value, params_str, 3, 1)
            else:
                self._write_value_based_on_mode(third_param_value, params_str, 3, 0)
            self.instruction_pointer += 4
            return

        if opcode == 8:
            second_param_value = self._get_value_in_memory_fallback_0(self.instruction_pointer + 2)
            third_param_value = self._get_value_in_memory_fallback_0(self.instruction_pointer + 3)

            first_param = self._get_value_based_on_mode(first_param_value, params_str, 1)
            second_param = self._get_value_based_on_mode(second_param_value, params_str, 2)
            if first_param == second_param:
                self._write_value_based_on_mode(third_param_value, params_str, 3, 1)
            else:
                self._write_value_based_on_mode(third_param_value, params_str, 3, 0)
            self.instruction_pointer += 4
            return

        if opcode == 9:
            self.relative_base += self._get_value_based_on_mode(first_param_value, params_str, 1)
            self.instruction_pointer += 2
            return

        raise AttributeError(
            "the opcode found at index " + str(self.instruction_pointer) + ", " + str(opcode) + " isn't a valid opcode")

    def _get_value_in_memory_fallback_0(self, param_value):
        if param_value in self.memory:
            return self.memory[param_value]
        return 0

    def _get_value_based_on_mode(self, param_value, parameters_str, index_param):
        try:
            mode = int(parameters_str[-index_param])
        except IndexError:
            mode = 0
        if mode == 0:
            return self._get_value_in_memory_fallback_0(param_value)
        if mode == 1:
            return param_value
        if mode == 2:
            return self._get_value_in_memory_fallback_0(param_value + self.relative_base)

        raise AttributeError("unrecognised parameter mode, ", str(mode))

    def _write_value_based_on_mode(self, param_value, parameters_str, index_param, value_to_write):
        try:
            mode = int(parameters_str[-index_param])
        except IndexError:
            mode = 0
        if mode == 0:
            self.memory[param_value] = value_to_write
        elif mode == 1:
            raise AttributeError("unrecognised parameter mode, can't write in mode 1", str(mode))
        elif mode == 2:
            self.memory[param_value + self.relative_base] = value_to_write
        else:
            raise AttributeError("unrecognised parameter mode, ", str(mode))
