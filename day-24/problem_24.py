"""

"""


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) + abs(a[3] - b[3])


class Constellation:
    def __init__(self, point):
        self.points = {point}

    def add_point(self, new_point):
        self.points.add(new_point)

    def check_in_constellation(self, candidate):
        for point in self.points:
            if manhattan(point, candidate) <= 3:
                return True

        return False

    def merge_constellation(self, constellation):
        self.points = self.points.union(constellation.points)


if __name__ == '__main__':
    points = []
    with open('input', 'r') as file:
        for line in file:
            if len(line) > 0:
                points.append(tuple([int(x) for x in line.replace('\n', '').split(',')]))

    constellations = list()
    for point in points:
        indices = list()

        for i, constellation in enumerate(constellations):
            if constellation.check_in_constellation(point):
                indices.append(i)

        if len(indices) == 0:
            constellations.append(Constellation(point))
        else:
            constellations[indices[0]].add_point(point)

            merge_into = indices[0]
            merge_from = indices[1:][::-1]
            while len(merge_from) != 0:
                constellations[merge_into].merge_constellation(constellations[merge_from[0]])
                del constellations[merge_from[0]]
                del merge_from[0]

    print(f'Answer 1 is {len(constellations)}')
