"""
The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

What is the size of the largest area that isn't infinite

--- Part Two ---

On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.

What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?
"""

import numpy as np


def manhattan_distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def closest_index(x, points):
    closest_distance = 10**12
    closest_point = None
    for point in points:
        distance = manhattan_distance(x, point)
        if distance < closest_distance:
            closest_distance = distance
            closest_point = point
        elif distance == closest_distance:
            closest_point = [-1, -1, -1]
    return closest_point[2]


def total_distance(x, points):
    total = 0
    for point in points:
        total += manhattan_distance(point, x)
    return total


if __name__ == "__main__":
    # Read input.
    with open("input", "r") as file:
        points = []
        for line in file:
            points.append([int(x) for x in line.replace("\n", "").split(",")])

    # Add a point ID to deal with identical points later on.
    for index, _ in enumerate(points):
        points[index] = points[index] + [index + 1]

    # Create a box with a safeish boundary.
    max_index = max([x[0] for x in points] + [x[1] for x in points]) * 4
    box = np.zeros(shape=(max_index, max_index))

    # Shift the coordinates to be nice and in the box.
    points = [[x[0] + (max_index / 2), x[1] + (max_index / 2), x[2]] for x in points]

    # Floodfill the box. Initially I missed that this Manhattan distance.
    for x in range(max_index):
        for y in range(max_index):
            box[x][y] = closest_index([x, y], points)

    # Create a list of candidates that do not touch the edge.
    ignore = set([-1])
    for x in range(max_index):
        ignore.add(box[x][0])
        ignore.add(box[x][max_index - 1])
    for y in range(max_index):
        ignore.add(box[0][y])
        ignore.add(box[max_index - 1][y])

    # Iterate over candidates and find the largest area.
    largest_area = 0
    unique, counts = np.unique(box, return_counts=True)
    for value, count in zip(unique, counts):
        if count > largest_area and value not in ignore:
            largest_area = count
    print(f"Answer 1 is {largest_area} squares.")

    # We iterate again over the box with the new condition.
    for x in range(max_index):
        for y in range(max_index):
            score = total_distance([x, y], points)
            if score < 10000:
                box[x][y] = 1
            else:
                box[x][y] = -1

    # Count.
    unique, counts = np.unique(box, return_counts=True)
    dict_version = dict(zip(unique, counts))
    safe_area = dict_version[1]
    print(f"Answer 2 is {safe_area} squares.")
