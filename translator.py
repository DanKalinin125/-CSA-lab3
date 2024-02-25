import sys
import json
from isa import Opcode, write_code, branch_instructions, zero_parameters_instructions, one_parameter_instructions, \
    two_parameter_instructions


def command_to_opcode(command):
    """Отображение операторов исходного кода в коды операций."""

    return {
        "nop": Opcode.NOP,
        "hlt": Opcode.HLT,
        "inc": Opcode.INC,
        "dec": Opcode.DEC,
        "add": Opcode.ADD,
        "sub": Opcode.SUB,
        "mov": Opcode.MOV,
        "test": Opcode.TEST,
        "jg": Opcode.JG,
        "jz": Opcode.JZ,
        "jnz": Opcode.JNZ,
        "jmp": Opcode.JMP,
    }.get(command, Opcode.NOP)


def read_asm(source_filename: str) -> list[str]:
    """Прочитать код из файла asm

        Возвращает список строк из указанного файла,
        удаляются отступы в начале и конце строки,
        удалаются пустые строки
    """

    lines = []
    with open(source_filename) as file:
        for line in file:
            line = line.strip()
            if line != "":
                lines.append(line)
    return lines


def delete_comments(lines: list[str]) -> list[str]:
    """Удалить комментарии из кода

        Распознает и удаляет из кода комментарии,
        т.е. все символы после и включая ';'
    """

    lines_without_comments = []
    for line in lines:
        comment_index = line.find(';')
        if comment_index == -1:
            lines_without_comments.append(line)
        elif comment_index != 0:
            line = line[:comment_index]
            line = line.strip()
            lines_without_comments.append(line)
    return lines_without_comments


def is_label(line: str) -> bool:
    return line.endswith(":")


def is_word(line: str) -> bool:
    return line.startswith(".word")


def word_is_str(word: str) -> bool:
    return word.startswith("'") and word.endswith("'")


PROGRAM_START_POSITION_IN_MEMORY = 4  # Считается, что до этого хранится служебная информация, изменение которой
# недопустимо


def find_labels(lines: list[str]) -> dict:
    labels = {}  # Хранит по ключ label_name значение label_position
    position = PROGRAM_START_POSITION_IN_MEMORY
    for line in lines:
        if is_label(line):  # Строка соответствует метке
            assert line not in labels, "Code error: label redefinition"
            labels[line[:-1]] = position

        elif is_word(line):  # Строка соответствует данным
            word = line[6::]
            if word_is_str(word):  # Данные строкового типа
                position += len(word[1:-1]) + 1  # +1, так как считаем нуль-терминатор
            else:  # Данные числового типа
                position += 1

        else:  # Строка соответствует команде
            position += 1
    return labels


def find_words(lines: list[str], labels: dict) -> list:
    words = []
    position = PROGRAM_START_POSITION_IN_MEMORY
    for line in lines:
        if is_word(line):  # Строка соответствует данным
            word = line[6::]
            if word_is_str(word):  # Данные строкового типа
                for symbol in word[1:-1]:
                    words.append({
                        "index": position,
                        "opcode": Opcode.NOP,
                        "arg_1": str(ord(symbol)),
                        "is_indirect_1": False,
                        "arg_2": None,
                        "is_indirect_2": None
                    })
                    position += 1

                words.append({
                    "index": position,
                    "opcode": Opcode.NOP,
                    "arg_1": str(0),
                    "is_indirect_1": False,
                    "arg_2": None,
                    "is_indirect_2": None
                })
                position += 1

            elif word.isdigit():  # Данные числового типа
                words.append({
                    "index": position,
                    "opcode": Opcode.NOP,
                    "arg_1": word,
                    "is_indirect_1": False,
                    "arg_2": None,
                    "is_indirect_2": None
                })
                position += 1

            elif word in labels:
                words.append({
                    "index": position,
                    "opcode": Opcode.NOP,
                    "arg_1": str(labels[word]),
                    "is_indirect_1": False,
                    "arg_2": None,
                    "is_indirect_2": None
                })
                position += 1

            else:
                raise AssertionError(f'Code error: incorrect word "{word}" in line "{line}"')

        elif not(is_label(line)):  # Строка соответствует команде
            position += 1

    return words


REGISTERS = ["r0", "r1", "r2", "r3"]


def parse_arg(arg: str, opcode: Opcode, labels: dict) -> tuple[str, bool]:
    if arg.startswith("(") and arg.endswith(")"):
        is_indirect = True
        arg = arg[1:-1]
    else:
        is_indirect = False

    assert arg.isdigit() or arg in labels or arg in REGISTERS, f'Code error: missing address {arg}'

    if arg in labels:
        assert opcode == Opcode.MOV or opcode in branch_instructions, f'Code error: for the {str(opcode)} command, only ' \
                                    f'register-to-register operations are allowed'
        arg = str(labels[arg])

    return arg, is_indirect


def parse_command_to_code(line: str, labels: dict):
    command = line.split(" ")[0]
    opcode = command_to_opcode(command)
    assert opcode != Opcode.NOP, f'Code error: there is no such command {command}'

    arg_1 = None
    is_indirect_1 = None
    arg_2 = None
    is_indirect_2 = None

    if command in zero_parameters_instructions:
        assert len(line.split(" ")) == 1, f'Code error: the command {command} must have 0 arguments'

    elif command in branch_instructions or command in one_parameter_instructions:
        assert len(line[len(command) + 1::].split(", ")) == 1, f'Code error: the command {command} must have 1 argument '
        arg_1, is_indirect_1 = parse_arg(line[len(command) + 1::].split(", ")[0], opcode, labels)

    elif command in two_parameter_instructions:
        assert len(line[len(command) + 1::].split(", ")) == 2, f'Code error: the command {command} must have 2 argument'
        args = line[len(command) + 1::].split(", ")
        arg_1, is_indirect_1 = parse_arg(args[0], opcode, labels)
        arg_2, is_indirect_2 = parse_arg(args[1], opcode, labels)

    return opcode, arg_1, is_indirect_1, arg_2, is_indirect_2


def find_code(lines: list[str], labels: dict) -> list:
    code = []
    position = PROGRAM_START_POSITION_IN_MEMORY
    for line in lines:
        if not(is_label(line) or is_word(line)): # Строка соответствует команде
            opcode, arg_1, is_indirect_1, arg_2, is_indirect_2 = parse_command_to_code(line, labels)
            code.append({
                "index": position,
                "opcode": opcode,
                "arg_1": arg_1,
                "is_indirect_1": is_indirect_1,
                "arg_2": arg_2,
                "is_indirect_2": is_indirect_2
            })
            position += 1

        elif is_word(line):  # Строка соответствует данным
            word = line[6::]
            if word_is_str(word):  # Данные строкового типа
                position += len(word[1:-1]) + 1  # +1, так как считаем нуль-терминатор
            else:  # Данные числового типа
                position += 1
    return code



def main(source_filename: str, target_filename: str):
    lines = read_asm(source_filename)

    lines = delete_comments(lines)

    labels = find_labels(lines)
    words = find_words(lines, labels)
    code = find_code(lines, labels)

    # Добавить определение метки _start

    for word in words:
        print(word)

    for c in code:
        print(c)


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Wrong arguments: translator.py <input_file> <target_file>"
    _, source_filename, target_filename = sys.argv
    main(source_filename, target_filename)
