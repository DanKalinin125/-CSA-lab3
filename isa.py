import json
from enum import Enum


class Opcode(str, Enum):
    NOP = "nop"
    HLT = "hlt"

    INC = "inc"
    DEC = "dec"
    ADD = "add"
    SUB = "sub"
    MOV = "mov"
    TEST = "test"

    JG = "jg"
    JZ = "jz"
    JNZ = "jnz"
    JMP = "jmp"

    def __str__(self) -> str:
        return str(self.value)


branch_instructions = [Opcode.JG, Opcode.JZ, Opcode.JNZ, Opcode.JMP]

two_parameter_instructions = [Opcode.ADD, Opcode.SUB, Opcode.MOV]

one_parameter_instructions = [Opcode.INC, Opcode.DEC]

zero_parameters_instructions = [Opcode.NOP, Opcode.HLT]


def write_code(filename: str, code):
    with open(filename, "w", encoding="utf-8") as file:
        buf = []
        for instr in code:
            buf.append(json.dumps(instr))
        file.write("[" + ",\n ".join(buf) + "]")


def read_code(filename: str):
    with open(filename, encoding="utf-8") as file:
        return json.loads(file.read())
