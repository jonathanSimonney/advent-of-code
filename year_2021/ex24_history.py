from dataclasses import dataclass
from enum import Enum, auto
from typing import Union, Callable, TypedDict


class InstructionsTypes(Enum):
    INP = auto()
    ADD = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    EQL = auto()


class AluVars(Enum):
    W = auto()
    X = auto()
    Y = auto()
    Z = auto()


dict_letter_to_alu_var = {
    'w': AluVars.W,
    'x': AluVars.X,
    'y': AluVars.Y,
    'z': AluVars.Z,
}


class SimplifiedParam(TypedDict):
    z_divisor: int
    x_add: int
    z_eventual_add: int


@dataclass(frozen=True)
class AluInstruction:
    instruction_type: InstructionsTypes
    instruction_param_1: AluVars
    instruction_param_2: Union[int, AluVars, None]


@dataclass(frozen=True)
class ZPossibleNum:
    min_remainder: int
    max_remainder: int
    nb_26_multiplicateurs_applied: int
    parent_z: Union['ZPossibleNum', None]
    child_z_1: Union['ZPossibleNum', None]
    child_z_2: Union['ZPossibleNum', None]


class AluProgram:
    w_var: int
    x_var: int
    y_var: int
    z_var: int
    max_z_number: int
    values_prompter: Callable[[], int]

    # return -1 if the program could be done compltely, or the rank of the digit at which it was determined 0 was unreachable
    def execute_simplified_program(self, list_instructions: list[SimplifiedParam], values_prompter: Callable[[], int]) -> int:
        self._init_variables(values_prompter)

        rank_digit = 0
        for instruction in list_instructions:
            rank_digit += 1
            can_keep_going = self._execute_simplified_instruction(instruction)
            if not can_keep_going:
                return rank_digit

        return -1

    def execute_program(self, list_instructions: list[AluInstruction], values_prompter: Callable[[], int]) -> None:
        self._init_variables(values_prompter)
        for instruction in list_instructions:
            self._execute_instruction(instruction)

    def _init_variables(self, values_prompter: Callable[[], int]):
        self.w_var = 0
        self.x_var = 0
        self.y_var = 0
        self.z_var = 0
        self.max_z_number = 26**7
        self.values_prompter = values_prompter

    def _execute_simplified_instruction(self, instruction: SimplifiedParam) -> bool:
        x_var = self.z_var % 26 + instruction['x_add']
        self.z_var = int(self.z_var / instruction['z_divisor'])

        input_user = self.values_prompter()

        if 0 < x_var < 10:
            print(f"overriding current candidate with {x_var}")
            input_user = self.x_var
        if x_var != input_user:
            self.z_var = 26 * self.z_var + input_user + instruction['z_eventual_add']

        if instruction['z_divisor'] == 26:
            self.max_z_number /= 26

        if self.z_var > self.max_z_number:
            return False

        return True

    def _execute_instruction(self, instruction: AluInstruction):
        if instruction.instruction_type == InstructionsTypes.INP:
            self._execute_input(instruction.instruction_param_1, self.values_prompter())
        elif instruction.instruction_type == InstructionsTypes.ADD:
            self._execute_add(instruction.instruction_param_1, instruction.instruction_param_2)
        elif instruction.instruction_type == InstructionsTypes.MUL:
            self._execute_mul(instruction.instruction_param_1, instruction.instruction_param_2)
        elif instruction.instruction_type == InstructionsTypes.DIV:
            self._execute_div(instruction.instruction_param_1, instruction.instruction_param_2)
        elif instruction.instruction_type == InstructionsTypes.MOD:
            self._execute_mod(instruction.instruction_param_1, instruction.instruction_param_2)
        elif instruction.instruction_type == InstructionsTypes.EQL:
            self._execute_eql(instruction.instruction_param_1, instruction.instruction_param_2)
        else:
            raise AttributeError("not a valid alu instruction")

    def _execute_input(self, param_1: AluVars, value_to_store: int):
        self._set_var_value(param_1, value_to_store)

    def _execute_add(self, param_1: AluVars, param_2: Union[int, AluVars, None]):
        self._set_var_value(param_1, self._get_var_value(param_1) + self._get_var_value(param_2))

    def _execute_mul(self, param_1: AluVars, param_2: Union[int, AluVars, None]):
        self._set_var_value(param_1, self._get_var_value(param_1) * self._get_var_value(param_2))

    def _execute_div(self, param_1: AluVars, param_2: Union[int, AluVars, None]):
        self._set_var_value(param_1, int(self._get_var_value(param_1) / self._get_var_value(param_2)))

    def _execute_mod(self, param_1: AluVars, param_2: Union[int, AluVars, None]):
        self._set_var_value(param_1, int(self._get_var_value(param_1) % self._get_var_value(param_2)))

    def _execute_eql(self, param_1: AluVars, param_2: Union[int, AluVars, None]):
        value_1 = self._get_var_value(param_1)
        value_2 = self._get_var_value(param_2)
        self._set_var_value(param_1, 1 if value_1 == value_2 else 0)

    def _set_var_value(self, enum_var: AluVars, value_to_store: int):
        if enum_var is AluVars.W:
            self.w_var = value_to_store
        elif enum_var is AluVars.X:
            self.x_var = value_to_store
        elif enum_var is AluVars.Y:
            self.y_var = value_to_store
        elif enum_var is AluVars.Z:
            self.z_var = value_to_store
        else:
            raise AttributeError("not a valid alu var")

    def _get_var_value(self, var_union: Union[int, AluVars, None]) -> int:
        if var_union is None:
            raise AttributeError("no value associated to None")
        if isinstance(var_union, int):
            return var_union
        if var_union is AluVars.W:
            return self.w_var
        elif var_union is AluVars.X:
            return self.x_var
        elif var_union is AluVars.Y:
            return self.y_var
        elif var_union is AluVars.Z:
            return self.z_var
        else:
            raise AttributeError("not a valid alu var")


def parse_line(line_to_parse: str) -> AluInstruction:
    line_list = line_to_parse.split(" ")
    type_instruction: InstructionsTypes
    if line_list[0] == 'inp':
        type_instruction = InstructionsTypes.INP
    elif line_list[0] == 'add':
        type_instruction = InstructionsTypes.ADD
    elif line_list[0] == 'mul':
        type_instruction = InstructionsTypes.MUL
    elif line_list[0] == 'div':
        type_instruction = InstructionsTypes.DIV
    elif line_list[0] == 'mod':
        type_instruction = InstructionsTypes.MOD
    elif line_list[0] == 'eql':
        type_instruction = InstructionsTypes.EQL
    else:
        raise AttributeError(f"no type found correpsonding to {line_list[0]}")

    param_instruction_1 = dict_letter_to_alu_var[line_list[1]]
    param_instruction_2: Union[AluVars, int, None]
    if len(line_list) == 2:
        param_instruction_2 = None
    else:
        param_instruction_2 = dict_letter_to_alu_var[line_list[2]] \
            if line_list[2] in dict_letter_to_alu_var.keys() else int(line_list[2])

    return AluInstruction(type_instruction, param_instruction_1, param_instruction_2)


def make_prompter_for_given_number(number_to_prompt: str) -> Callable[[], int]:
    nb_call_done: int = 0

    def prompt_a_num():
        nonlocal nb_call_done
        nb_to_ret = number_to_prompt[nb_call_done]
        nb_call_done += 1

        # print(f"returned number {nb_to_ret}")
        return int(nb_to_ret)

    return prompt_a_num


# list params more easy :
list_params: list[SimplifiedParam] = [
    {
        "z_divisor": 1,
        "x_add": 11,
        "z_eventual_add": 8
    },
    {
        "z_divisor": 1,
        "x_add": 14,
        "z_eventual_add": 13
    },
    {
        "z_divisor": 1,
        "x_add": 10,
        "z_eventual_add": 2
    },
    {
        "z_divisor": 26,
        "x_add": 0,
        "z_eventual_add": 7
    },
    {
        "z_divisor": 1,
        "x_add": 12,
        "z_eventual_add": 11
    },
    {
        "z_divisor": 1,
        "x_add": 12,
        "z_eventual_add": 4
    },
    {
        "z_divisor": 1,
        "x_add": 12,
        "z_eventual_add": 13
    },
    {
        "z_divisor": 26,
        "x_add": -8,
        "z_eventual_add": 13
    },
    {
        "z_divisor": 26,
        "x_add": -9,
        "z_eventual_add": 10
    },
    {
        "z_divisor": 1,
        "x_add": 11,
        "z_eventual_add": 1
    },
    {
        "z_divisor": 26,
        "x_add": 0,
        "z_eventual_add": 2
    },
    {
        "z_divisor": 26,
        "x_add": -5,
        "z_eventual_add": 14
    },
    {# 1 : z = [7,15]
        #2 : z = [26*13, 26*21] + [7, 15]
        "z_divisor": 26,
        "x_add": -6,
        "z_eventual_add": 6
    },# 1 : z was = 0, input_user = [7, 9]
    # 2 : z was != 0 (ergo, z = [26*13, 26*22], input_user = self.x_var,
    { # z = [13, 22]
        "z_divisor": 26,
        "x_add": -12,
        "z_eventual_add": 14
    } # z = 0, #x = [1, 9]
    # z = 26 * z' + R (with R = [1, 25])
]

bottom_z: ZPossibleNum = ZPossibleNum(13, 21, 0, None, None, None)


def main():
    with open("data.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [parse_line(line.strip()) for line in content]

    alu_program = AluProgram()

    test_model_number = '99999999999999'

    while True:
        # print(test_model_number)
        rank_breaking = alu_program.execute_simplified_program(list_params, make_prompter_for_given_number(test_model_number.zfill(14)))
        if alu_program.z_var == 0:
            break

        if rank_breaking == -1:
            test_model_number = str(int(test_model_number) - 1)
        else:
            number_tested_as_list = list(test_model_number)

            # print(number_tested_as_list)
            #
            # print(rank_breaking, number_tested_as_list[:rank_breaking], number_tested_as_list[rank_breaking:])
            first_part_number = int(''.join(number_tested_as_list[:rank_breaking]))
            len_second_part_number = 14 - rank_breaking

            # print(rank_breaking, first_part_number, second_part_number)
            # number_tested_as_list[rank_breaking - 1] = str(int(number_tested_as_list[rank_breaking - 1]) - 1)
            test_model_number = str(first_part_number - 1) + '9' * len_second_part_number
        print(test_model_number)

    print(test_model_number)


if __name__ == "__main__":
    main()

# tactique : remonter la liste de Z en partant du bas, ça fera 2**14 possibilité, nettement moins que les 9**14
# possibilités pour la structure d'un z, besoin : le parent, les 2 enfants, le nb de multiplicateurs 26 qu'on a qui
# traînent, et le reste (derrière tt les multiplicateurs de 26 quoi)

# MONAD current state :
# W inp_2
# X 0
# Y inp_1 + 8
# Z 0
