"""
The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

What is the size of the largest area that isn't infinite?
"""


if __name__ == '__main__':
    # Read input.
    with open('input', 'r') as file:
        points = []
        for line in file:
            points.append([int(x) for x in line.replace('\n', '').split(',')])

    # Add a point ID to deal with identical points later on.
    for index, _ in enumerate(points):
        points[index] = points[index] + [index]

    # Create a box with a safeish boundary.

    # Shift the coordinates to be nice and in the box.

    # Floodfill the box.

    # Create a list of candidates that do not touch the edge.

    # Iterate over candidates and find the largest area.

    print(f'Answer 1 is {largest_area} squares.')
