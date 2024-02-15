from typing import Generator


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(f"{self.x},{self.y}")

    @classmethod
    def parse(cls, input_, delimiter):
        args = [int(x) for x in input_.split(delimiter)]
        return Point(*args)

    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x and self.y == other.y

    def manhattan_distance(self, other: "Point"):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def neighborhood(self) -> Generator["Point", None, None]:
        deltas = (-1, 0, 1)
        for xd in deltas:
            for yd in deltas:
                if xd == 0 and yd == 0:
                    continue
                yield Point(self.x + xd, self.y + yd)
