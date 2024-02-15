from src.day_protocol import AocDay


class Day1(AocDay):
    @staticmethod
    def _parse(input_: str):
        values = []
        for row in input_.split("\n"):
            if row:
                values.append(int(row))
        return values

    def part_a(self, input_: str) -> str:
        values = self._parse(input_)
        return str(sum(values))

    def part_b(self, input_: str) -> str:
        values = self._parse(input_)
        frequency = 0
        visited_values = set()
        visited_values.add(frequency)
        while True:
            for value in values:
                frequency += value
                if frequency in visited_values:
                    return str(frequency)
                visited_values.add(frequency)
