"""
The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

What is the size of the largest area that isn't infinite?
"""



def angle_clockwise(A, B):


def convex_hull(input_points):
    # Pick leftmost index.
    left_index = 0
    left_value = input_points[0][0]
    for i, value in enumerate(input_points):
        if input_points[i][0] < left_value:
            left_index = i
            left_value = input_points[i][0]
            input_points[i][0]

    # Start the hull.
    last_line = ((input_points[left_index][0], input_points[left_index][0]),
                  input_points[left_index])
    hull = [left_index]
    while (hull[0] != hull[-1] or len(hull) == 1) and len(input_points) != 1:
        smallest_angle = 360
        smallest_id = None

        for i, value in enumerate(input_points):
            if i == hull[-1]:
                continue
            angle = angle_clockwise(last_line, ((input_points[hull[-1]], input_points[i])))
            if angle < smallest_angle:
                smallest_angle = angle
                smallest_id = id

        last_line = (input_points[hull[-1]], input_points[smallest_Id])
        hull.append(smallest_id)

    return hull


if __name__ == '__main__':
    # Read input.
    with open('input', 'r') as file:
        points = []
        for line in file:
            points.append(tuple([int(x) for x in line.replace('\n', '').split(',')]))

    # Exclude the convex hull.

    print(convex_hull(points))
