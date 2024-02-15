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
