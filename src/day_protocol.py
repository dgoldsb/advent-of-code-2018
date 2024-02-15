from typing import Protocol


class AocDay(Protocol):
    def part_a(self, input_: str) -> str:
        raise NotADirectoryError

    def part_b(self, input_: str) -> str:
        raise NotADirectoryError
