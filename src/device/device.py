from dataclasses import dataclass
from typing import Callable

from src.device import *


@dataclass
class Instruction:
    fun: Callable
    args: tuple[int, ...]

    def apply(self, register: list[int, ...]):
        return self.fun(register, *self.args)


class Device:
    _OPCODE_MAP = {
        "addr": addr,
        "addi": addi,
        "mulr": mulr,
        "muli": muli,
        "banr": banr,
        "bani": bani,
        "borr": borr,
        "bori": bori,
        "setr": setr,
        "seti": seti,
        "gtir": gtir,
        "gtri": gtri,
        "gtrr": gtrr,
        "eqir": eqir,
        "eqri": eqri,
        "eqrr": eqrr,
    }

    def __init__(self, program: str):
        self._instruction_pointer_binding = None
        self._instructions = []

        for line in program.split("\n"):
            if "#ip" in line:
                self._instruction_pointer_binding = int(line.replace("#ip ", ""))
            else:
                opcode, *args = line.split(" ")

                self._instructions.append(
                    Instruction(self._OPCODE_MAP[opcode], tuple(int(a) for a in args))
                )

    def run(self, register: list):
        instruction_pointer = 0

        while True:
            try:
                instruction = self._instructions[instruction_pointer]
            except IndexError:
                break

            # Write instruction pointer to register.
            if instruction_pointer is not None:
                register[self._instruction_pointer_binding] = instruction_pointer

            register = instruction.apply(register)

            # Read instruction pointer from register.
            if self._instruction_pointer_binding is not None:
                instruction_pointer = register[self._instruction_pointer_binding]

            instruction_pointer += 1

        return register
