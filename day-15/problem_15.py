"""
According to the manual, the device has four registers (numbered 0 through 3) that can be manipulated by instructions containing one of 16 opcodes. The registers start with the value 0.

Every instruction consists of four values: an opcode, two inputs (named A and B), and an output (named C), in that order. The opcode specifies the behavior of the instruction and how the inputs are interpreted. The output, C, is always treated as a register.

In the opcode descriptions below, if something says "value A", it means to take the number given as A literally. (This is also called an "immediate" value.) If something says "register A", it means to use the number given as A to read from (or write to) the register with that number. So, if the opcode addi adds register A and value B, storing the result in register C, and the instruction addi 0 7 3 is encountered, it would add 7 to the value contained by register 0 and store the sum in register 3, never modifying registers 0, 1, or 2 in the process.

Many opcodes are similar except for how they interpret their arguments. The opcodes fall into seven general categories:

Addition:

    addr (add register) stores into register C the result of adding register A and register B.
    addi (add immediate) stores into register C the result of adding register A and value B.

Multiplication:

    mulr (multiply register) stores into register C the result of multiplying register A and register B.
    muli (multiply immediate) stores into register C the result of multiplying register A and value B.

Bitwise AND:

    banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
    bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.

Bitwise OR:

    borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
    bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.

Assignment:

    setr (set register) copies the contents of register A into register C. (Input B is ignored.)
    seti (set immediate) stores value A into register C. (Input B is ignored.)

Greater-than testing:

    gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
    gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
    gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.

Equality testing:

    eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
    eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
    eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.

Unfortunately, while the manual gives the name of each opcode, it doesn't seem to indicate the number. However, you can monitor the CPU to see the contents of the registers before and after instructions are executed to try to work them out. Each opcode has a number from 0 through 15, but the manual doesn't say which is which. For example, suppose you capture the following sample:

Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]

This sample shows the effect of the instruction 9 2 1 2 on the registers. Before the instruction is executed, register 0 has value 3, register 1 has value 2, and registers 2 and 3 have value 1. After the instruction is executed, register 2's value becomes 2.

The instruction itself, 9 2 1 2, means that opcode 9 was executed with A=2, B=1, and C=2. Opcode 9 could be any of the 16 opcodes listed above, but only three of them behave in a way that would cause the result shown in the sample:

    Opcode 9 could be mulr: register 2 (which has a value of 1) times register 1 (which has a value of 2) produces 2, which matches the value stored in the output register, register 2.
    Opcode 9 could be addi: register 2 (which has a value of 1) plus value 1 produces 2, which matches the value stored in the output register, register 2.
    Opcode 9 could be seti: value 2 matches the value stored in the output register, register 2; the number given for B is irrelevant.

None of the other opcodes produce the result captured in the sample. Because of this, the sample above behaves like three opcodes.

You collect many of these samples (the first section of your puzzle input). The manual also includes a small test program (the second section of your puzzle input) - you can ignore it for now.

Ignoring the opcode numbers, how many samples in your puzzle input behave like three or more opcodes?

--- Part Two ---

Using the samples you collected, work out the number of each opcode and execute the test program (the second section of your puzzle input).

What value is contained in register 0 after executing the test program?
"""

from copy import copy


def addr(reg, a, b, c):
    reg[c] = reg[a] + reg[b]
    return reg


def addi(reg, a, b, c):
    reg[c] = reg[a] + b
    return reg


def mulr(reg, a, b, c):
    reg[c] = reg[a] * reg[b]
    return reg


def muli(reg, a, b, c):
    reg[c] = reg[a] * b
    return reg


def banr(reg, a, b, c):
    reg[c] = reg[a] & reg[b]
    return reg


def bani(reg, a, b, c):
    reg[c] = reg[a] & b
    return reg


def borr(reg, a, b, c):
    reg[c] = reg[a] | reg[b]
    return reg


def bori(reg, a, b, c):
    reg[c] = reg[a] | b
    return reg


def setr(reg, a, b, c):
    reg[c] = reg[a]
    return reg


def seti(reg, a, b, c):
    reg[c] = a
    return reg


def gtir(reg, a, b, c):
    reg[c] = 1 if a > reg[b] else 0
    return reg


def gtri(reg, a, b, c):
    reg[c] = 1 if reg[a] > b else 0
    return reg


def gtrr(reg, a, b, c):
    reg[c] = 1 if reg[a] > reg[b] else 0
    return reg


def eqir(reg, a, b, c):
    reg[c] = 1 if a == reg[b] else 0
    return reg


def eqri(reg, a, b, c):
    reg[c] = 1 if reg[a] == b else 0
    return reg


def eqrr(reg, a, b, c):
    reg[c] = 1 if reg[a] == reg[b] else 0
    return reg


if __name__ == "__main__":
    # Set the functions without params.
    funs = [
        addr,
        addi,
        mulr,
        muli,
        banr,
        bani,
        borr,
        bori,
        setr,
        seti,
        gtir,
        gtri,
        gtrr,
        eqir,
        eqri,
        eqrr,
    ]

    # Iterate over the input.
    opcodes = dict()
    samples = dict()
    with open("input", "r") as file:
        sample = 0
        while True:
            x = file.readline()

            try:
                if x[0] != "B":
                    break
            except:
                break

            x = x.replace("Before: [", "").replace("]\n", "").split(", ")
            y = file.readline().replace("\n", "").split(" ")
            z = file.readline().replace("After:  [", "").replace("]\n", "").split(", ")
            _ = file.readline()

            x = [int(a) for a in x]
            y = [int(a) for a in y]
            z = [int(a) for a in z]

            print(f"Opcode is {y[0]}.")
            if y[0] not in opcodes.keys():
                opcodes[y[0]] = [set(), set()]
            samples[sample] = set()

            for fun in funs:
                if fun(copy(x), y[1], y[2], y[3]) == z:
                    opcodes[y[0]][0].add(fun)
                    samples[sample].add(fun)
                else:
                    opcodes[y[0]][1].add(fun)
            sample += 1

        counter = 0
        for _, value in samples.items():
            if len(value) > 2:
                counter += 1
        print(f"Answer 1 is {counter}.")

        # Delete counterexamples from examples.
        for k in opcodes.keys():
            opcodes[k] = opcodes[k][0] - opcodes[k][1]

        # Find out what is what.
        while max([len(v) for v in opcodes.values()]) > 1:
            for k1, v1 in opcodes.items():
                if len(v1) == 1:
                    for k2 in opcodes.keys():
                        if k1 != k2:
                            opcodes[k2] = opcodes[k2] - v1
        for k in opcodes.keys():
            opcodes[k] = list(opcodes[k])[0]

        # Run the program.
        reg = [0, 0, 0, 0]
        done = False
        _ = file.readline()
        while True:
            x = file.readline()
            x = x.replace("\n", "").split(" ")

            try:
                x = [int(y) for y in x]
                done = True  # mark that we have found the input body
                reg = opcodes[x[0]](copy(reg), x[1], x[2], x[3])
            except:
                if done:
                    break
                else:
                    continue
        print(f"Answer 2 is {reg[0]}.")
