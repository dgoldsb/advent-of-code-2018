"""
You scan a two-dimensional vertical slice of the ground nearby and discover that it is mostly sand with veins of clay. The scan only provides data with a granularity of square meters, but it should be good enough to determine how much water is trapped there. In the scan, x represents the distance to the right, and y represents the distance down. There is also a spring of water near the surface at x=500, y=0. The scan identifies which square meters are clay (your puzzle input).

For example, suppose your scan shows the following veins of clay:

x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504

Rendering clay as #, sand as ., and the water spring as +, and with x increasing to the right and y increasing downward, this becomes:

   44444455555555
   99999900000000
   45678901234567
 0 ......+.......
 1 ............#.
 2 .#..#.......#.
 3 .#..#..#......
 4 .#..#..#......
 5 .#.....#......
 6 .#.....#......
 7 .#######......
 8 ..............
 9 ..............
10 ....#.....#...
11 ....#.....#...
12 ....#.....#...
13 ....#######...

The spring of water will produce water forever. Water can move through sand, but is blocked by clay. Water always moves down when possible, and spreads to the left and right otherwise, filling space that has clay on both sides and falling out otherwise.

For example, if five squares of water are created, they will flow downward until they reach the clay and settle there. Water that has come to rest is shown here as ~, while sand through which water has passed (but which is now dry again) is shown as |:

......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#....|#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...

Two squares of water can't occupy the same location. If another five squares of water are created, they will settle on the first five, filling the clay reservoir a little more:

......+.......
......|.....#.
.#..#.|.....#.
.#..#.|#......
.#..#.|#......
.#~~~~~#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...

Water pressure does not apply in this scenario. If another four squares of water are created, they will stay on the right side of the barrier, and no water will reach the left side:

......+.......
......|.....#.
.#..#.|.....#.
.#..#~~#......
.#..#~~#......
.#~~~~~#......
.#~~~~~#......
.#######......
..............
..............
....#.....#...
....#.....#...
....#.....#...
....#######...

At this point, the top reservoir overflows. While water can reach the tiles above the surface of the water, it cannot settle there, and so the next five squares of water settle like this:

......+.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
........|.....
....#...|.#...
....#...|.#...
....#~~~~~#...
....#######...

Note especially the leftmost |: the new squares of water can reach this tile, but cannot stop there. Instead, eventually, they all fall to the right and settle in the reservoir below.

After 10 more squares of water, the bottom reservoir is also full:

......+.......
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
........|.....
....#~~~~~#...
....#~~~~~#...
....#~~~~~#...
....#######...

Finally, while there is nowhere left for the water to settle, it can reach a few more tiles before overflowing beyond the bottom of the scanned data:

......+.......    (line not counted: above minimum y value)
......|.....#.
.#..#||||...#.
.#..#~~#|.....
.#..#~~#|.....
.#~~~~~#|.....
.#~~~~~#|.....
.#######|.....
........|.....
...|||||||||..
...|#~~~~~#|..
...|#~~~~~#|..
...|#~~~~~#|..
...|#######|..
...|.......|..    (line not counted: below maximum y value)
...|.......|..    (line not counted: below maximum y value)
...|.......|..    (line not counted: below maximum y value)

How many tiles can be reached by the water? To prevent counting forever, ignore tiles with a y coordinate smaller than the smallest y coordinate in your scan data or larger than the largest one. Any x coordinate is valid. In this example, the lowest y coordinate given is 1, and the highest is 13, causing the water spring (in row 0) and the water falling off the bottom of the render (in rows 14 through infinity) to be ignored.

So, in the example above, counting both water at rest (~) and other sand tiles the water can hypothetically reach (|), the total number of tiles the water can reach is 57.

How many tiles can the water reach within the range of y values in your scan?

--- Part Two ---

After a very long time, the water spring will run dry. How much water will be retained?

In the example above, water that won't eventually drain out is shown as ~, a total of 29 tiles.

How many water tiles are left after the water spring stops producing water and all remaining water not at rest has drained?
"""

import re

import numpy as np

MIN_X = None
GRID = np.ndarray(shape=(0, 0))
SPRING = [500, 0]
DEBUG = False


class Drop:
    def __init__(self, location=SPRING):
        self.x = location[0]
        self.y = location[1]
        if DEBUG:
            print(f"Spawn at {self.x},{self.y}.")

    def can_fall(self):
        return GRID[self.x][self.y + 1] in [0, 2]

    def can_spread(self):
        return (GRID[self.x - 1][self.y] in [0, 2]) or (
            GRID[self.x + 1][self.y] in [0, 2]
        )

    def fall(self):
        while True:
            if self.y + 1 == len(GRID[x]):
                # Return that this hit the end
                return True
            elif GRID[x][self.y + 1] == 100:
                return True
            elif not self.can_fall():
                break
            else:
                self.y += 1
                GRID[self.x][self.y] = 2

        return self.spread()

    def spread(self):
        children = []

        # Spread right.
        right_ended = False
        start_x = self.x
        start_y = self.y
        while True:
            if self.can_fall():
                new_drop = Drop([self.x, self.y])
                reached_end = new_drop.fall()
                if reached_end:
                    GRID[self.x][self.y] = 100  # create a sink
                    children.append(0)
                else:
                    children.append(1)
                break
            elif GRID[self.x + 1][self.y] == 100:
                children.append(0)
                right_ended = True
                break
            elif GRID[self.x + 1][self.y] == -1:
                break
            else:
                self.x += 1
                GRID[self.x][self.y] = 2

        # Spread left.
        left_ended = False
        self.x = start_x
        self.y = start_y
        while True:
            if self.can_fall():
                new_drop = Drop([self.x, self.y])
                reached_end = new_drop.fall()
                if reached_end:
                    GRID[self.x][self.y] = 100  # create a sink
                    children.append(0)
                else:
                    children.append(1)
                break
            elif GRID[self.x - 1][self.y] == 100:
                children.append(0)
                left_ended = True
                break
            elif GRID[self.x - 1][self.y] == -1:
                break
            else:
                self.x -= 1
                GRID[self.x][self.y] = 2

        if right_ended and left_ended:
            return True

        # If no children, spread still.
        if len(children) == 0:
            return self.still()
        else:
            if sum(children) > 0:
                return False
            else:
                return True

    def still(self):
        GRID[self.x][self.y] = 3

        while True:
            if GRID[self.x + 1][self.y] == -1:
                break
            else:
                self.x += 1
                GRID[self.x][self.y] = 3

        while True:
            if GRID[self.x - 1][self.y] == -1:
                break
            else:
                self.x -= 1
                GRID[self.x][self.y] = 3

        # Return that this did not reach a sink.
        return False


def print_grid():
    def map_to_char(a):
        if a == 1:
            return "+"
        elif a == -1:
            return "#"
        elif a == 0:
            return "."
        elif a == 100:
            return "s"
        elif a == 2:
            return "|"
        elif a == 3:
            return "~"

    for grid_line in list(np.transpose(GRID)):
        print("".join([map_to_char(a) for a in grid_line[MIN_X:]]))


def answer():
    unique, counts = np.unique(GRID, return_counts=True)
    dict_counts = dict(zip(unique, counts))
    total = dict_counts[2] + dict_counts[3] + dict_counts[100]
    print(f"Answer 1 is {total}.")
    print(f"Answer 1 is {dict_counts[3]}.")


if __name__ == "__main__":
    tiles = []
    with open("input", "r") as file:
        for line in file:
            match = re.match("([xy])=([0-9]+), ([xy])=([0-9]+)..([0-9]+)", line)
            if match:
                if match.group(1) == "x":
                    for y in range(int(match.group(4)), int(match.group(5)) + 1):
                        tiles.append((int(match.group(2)), y))
                elif match.group(1) == "y":
                    for x in range(int(match.group(4)), int(match.group(5)) + 1):
                        tiles.append((x, int(match.group(2))))

    # Create the grid.
    MIN_X = min([c[0] for c in tiles]) - 2
    min_y = min([c[1] for c in tiles])
    max_x = max([c[0] for c in tiles]) + 2
    max_y = max([c[1] for c in tiles]) + 1
    GRID = np.ndarray(shape=(max_x, max_y))
    for c in tiles:  # 1 is well, 2 is flowing, 3 is still, -1 is clay
        GRID[c[0], c[1]] = -1
    GRID[SPRING[0], SPRING[1]] = 1  # place the well

    # Loop until the drop and its children are dead.
    i = 0
    while True:
        grid_copy = np.copy(GRID)
        drop = Drop()

        # Evaluate the drop.
        if drop.can_fall():
            drop.fall()
        elif drop.can_spread():
            drop.spread()

        if DEBUG:
            print(f"Doing drop from well #{i}.")
        i += 1
        if np.array_equal(GRID, grid_copy):
            break

    # Print the endgame grid.
    smaller = [line[min_y:] for line in list(GRID)]
    GRID = np.array(smaller)
    print_grid()
    answer()
