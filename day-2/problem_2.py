"""
The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:

    The number of inches between the left edge of the fabric and the left edge of the rectangle.
    The number of inches between the top edge of the fabric and the top edge of the rectangle.
    The width of the rectangle in inches.
    The height of the rectangle in inches.

A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by # (and ignores the square inches of fabric represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........

The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2

Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........

The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?

--- Part Two ---

Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?
"""


if __name__=='__main__':
    # Create the cloth.
    size = 1100
    cloth = []
    for i in range(0, size):
        cloth_line = []
        for j in range(0, size):
            cloth_line.append(0)
        cloth.append(cloth_line)

    subcloths = []
    with open('input', 'r') as file:
        for line in file:
            unsplit_line = line.replace(' @ ', ',')
            unsplit_line = unsplit_line.replace(': ', ',')
            unsplit_line = unsplit_line.replace('x', ',')
            unsplit_line = unsplit_line.replace('\n', '')
            split_line = [int(x) for x in unsplit_line.split(',')[1:]]
            subcloths.append([split_line[0], split_line[1], split_line[2], split_line[3]])

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
    print('Answer 1 is {}.'.format(counter))

    # Find the ID of the subcloth that does not overlap with anything.
    for id, subcloth in enumerate(subcloths):
        found = True
        for i in range(subcloth[2]):
            for j in range(subcloth[3]):
                if cloth[subcloth[0] + i][subcloth[1] + j] != 1:
                    found = False
        if found:
            print('Answer 2 is {}'.format(value + 1))
