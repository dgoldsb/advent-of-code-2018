from src.day_protocol import AocDay
from src.space.point import Point

# Above the cutoff we assume it is infinite.
CUTOFF = 10_000


class Day6(AocDay):
    @staticmethod
    def _parse(input_: str) -> set[Point]:
        return {Point.parse(x, ", ") for x in input_.split("\n")}

    @staticmethod
    def find_closest_reference(point: Point, references: set[Point]) -> Point | None:
        closest = None
        closest_distance = CUTOFF * 2
        for reference in references:
            distance = point.manhattan_distance(reference)
            if distance < closest_distance:
                closest = reference
                closest_distance = distance
            elif distance == closest_distance:
                closest = None
        return closest

    def part_a(self, input_: str) -> str:
        biggest_non_infinite_area = 0

        references = self._parse(input_)
        for seed in references:
            visited = set()
            area = 0
            queued = {seed}
            to_visit = [seed]

            while to_visit:
                considered_point = to_visit.pop()
                queued.remove(considered_point)
                visited.add(considered_point)

                closest_reference = self.find_closest_reference(
                    considered_point, references
                )

                if closest_reference == seed:
                    area += 1
                    for neighbour in considered_point.neighborhood():
                        if neighbour not in visited and neighbour not in queued:
                            to_visit.append(neighbour)
                            queued.add(neighbour)

                if area == CUTOFF:
                    break

            if area != CUTOFF and area > biggest_non_infinite_area:
                biggest_non_infinite_area = area

        return str(biggest_non_infinite_area)

    def part_b(self, input_: str) -> str:
        references = self._parse(input_)
        counter = 0
        for x in range(-1000, 1000):
            for y in range(-1000, 1000):
                point = Point(x, y)

                if sum((point.manhattan_distance(r) for r in references)) < 10_000:
                    counter += 1
        return str(counter)
