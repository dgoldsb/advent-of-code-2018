from collections import defaultdict

from src.day_protocol import AocDay
from src.device import OPCODES


class Day16(AocDay):
    @staticmethod
    def _parse_samples(input_: str):
        samples = []

        for raw_sample in input_.split("\n\n"):
            try:
                raw_before, raw_operation, raw_after = raw_sample.split("\n")
            except ValueError:
                continue

            before = tuple(
                int(i)
                for i in raw_before.replace("Before: [", "")
                .replace("]", "")
                .split(", ")
            )
            operation = tuple(int(i) for i in raw_operation.split(" "))
            after = tuple(
                int(i)
                for i in raw_after.replace("After:  [", "").replace("]", "").split(", ")
            )

            samples.append((before, operation, after))

        return samples

    @staticmethod
    def _parse_test_program(input_: str):
        for line in input_.split("\n\n\n")[1].split("\n"):
            try:
                yield tuple(int(i) for i in line.split(" "))
            except:
                pass

    def part_a(self, input_: str) -> str:
        samples = self._parse_samples(input_)

        possible_opcodes = defaultdict(set)
        codes_per_sample = defaultdict(int)

        for index, sample in enumerate(samples):
            before, operation, after = sample
            opcode_number = operation[0]

            for opcode in OPCODES:
                if tuple(opcode(list(before), *operation[1:])) == after:
                    possible_opcodes[opcode_number].add(opcode)
                    codes_per_sample[index] += 1

        return str(sum((v > 2 for v in codes_per_sample.values())))

    def part_b(self, input_: str) -> str:
        samples = self._parse_samples(input_)

        possible_opcodes = defaultdict(set)
        impossible_opcodes = defaultdict(set)

        for index, sample in enumerate(samples):
            before, operation, after = sample
            opcode_number = operation[0]

            for opcode in OPCODES:
                if tuple(opcode(list(before), *operation[1:])) == after:
                    possible_opcodes[opcode_number].add(opcode)
                else:
                    impossible_opcodes[opcode_number].add(opcode)

        remaining_possible_opcodes = {
            k: possible_opcodes[k] - impossible_opcodes[k]
            for k in possible_opcodes.keys()
        }

        while any((len(v) > 1 for v in remaining_possible_opcodes.values())):
            for k, v in remaining_possible_opcodes.items():
                if len(v) == 1:
                    # Remove from other opcodes.
                    for other_key in remaining_possible_opcodes.keys():
                        if k != other_key:
                            try:
                                remaining_possible_opcodes[other_key] = (
                                    remaining_possible_opcodes[other_key] - v
                                )
                            except KeyError:
                                pass

        opcode_mapping = {k: v.pop() for k, v in remaining_possible_opcodes.items()}

        # Run the program.
        register = [0, 0, 0, 0]
        for command in self._parse_test_program(input_):
            register = opcode_mapping[command[0]](register, *command[1:])
        return str(register[0])
