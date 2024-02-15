from src.day_protocol import AocDay


class Day3(AocDay):
    def part_a(self, input_: str) -> str:
        # Create the cloth.
        size = 1100
        cloth = []
        for i in range(0, size):
            cloth_line = []
            for j in range(0, size):
                cloth_line.append(0)
            cloth.append(cloth_line)

        subcloths = []
        for line in input_.split("\n"):
            if line:
                unsplit_line = line.replace(" @ ", ",")
                unsplit_line = unsplit_line.replace(": ", ",")
                unsplit_line = unsplit_line.replace("x", ",")
                unsplit_line = unsplit_line.replace("\n", "")
                split_line = [int(x) for x in unsplit_line.split(",")[1:]]
                subcloths.append(
                    [split_line[0], split_line[1], split_line[2], split_line[3]]
                )

        # Loop over the subcloths.
        for subcloth in subcloths:
            # Add 1 to each of the relevant inches of the main cloth.
            for i in range(subcloth[2]):
                for j in range(subcloth[3]):
                    cloth[subcloth[0] + i][subcloth[1] + j] += 1

        # Count the number of inches that are used more than once.
        counter = 0
        for i in range(0, size):
            for j in range(0, size):
                if cloth[i][j] > 1:
                    counter += 1
        return str(counter)

    def part_b(self, input_: str) -> str:
        # Create the cloth.
        size = 1100
        cloth = []
        for i in range(0, size):
            cloth_line = []
            for j in range(0, size):
                cloth_line.append(0)
            cloth.append(cloth_line)

        subcloths = []
        for line in input_.split("\n"):
            if line:
                unsplit_line = line.replace(" @ ", ",")
                unsplit_line = unsplit_line.replace(": ", ",")
                unsplit_line = unsplit_line.replace("x", ",")
                unsplit_line = unsplit_line.replace("\n", "")
                split_line = [int(x) for x in unsplit_line.split(",")[1:]]
                subcloths.append(
                    [split_line[0], split_line[1], split_line[2], split_line[3]]
                )

        # Loop over the subcloths.
        for subcloth in subcloths:
            # Add 1 to each of the relevant inches of the main cloth.
            for i in range(subcloth[2]):
                for j in range(subcloth[3]):
                    cloth[subcloth[0] + i][subcloth[1] + j] += 1

        # Find the ID of the subcloth that does not overlap with anything.
        for id_, subcloth in enumerate(subcloths):
            found = True
            for i in range(subcloth[2]):
                for j in range(subcloth[3]):
                    if cloth[subcloth[0] + i][subcloth[1] + j] != 1:
                        found = False
            if found:
                return str(id_ + 1)
