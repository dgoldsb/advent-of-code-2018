from src.day_protocol import AocDay


def get_char_diff(v1, v2):
    diff = 0
    common = ""
    for counter, value in enumerate(v1):
        if value != v2[counter]:
            diff += 1
        else:
            common += value
    return diff, common


class Day2(AocDay):
    @staticmethod
    def _parse(input_: str):
        values = []
        for row in input_.split("\n"):
            if row:
                values.append(row)
        return values

    def part_a(self, input_: str) -> str:
        # Do the count.
        count_double = 0
        count_triple = 0
        for box_id in self._parse(input_):
            double_found = False
            triple_found = False
            for target in set(box_id):
                character_count = box_id.count(target)
                if character_count == 2:
                    double_found = True
                elif character_count == 3:
                    triple_found = True
            if double_found:
                count_double += 1
            if triple_found:
                count_triple += 1

        return str(count_double * count_triple)

    def part_b(self, input_: str) -> str:
        values = self._parse(input_)
        values.sort()
        for value_1 in values:
            for value_2 in values:
                diff, overlap = get_char_diff(value_1, value_2)
                if diff == 1:
                    return str(overlap)
        raise RuntimeError("No answer found!")
