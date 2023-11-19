"""
Each nanobot can transmit signals to any integer coordinate which is a distance away from it less than or equal to its signal radius (as measured by Manhattan distance). Coordinates a distance away of less than or equal to a nanobot's signal radius are said to be in range of that nanobot.

Before you start the teleportation process, you should determine which nanobot is the strongest (that is, which has the largest signal radius) and then, for that nanobot, the total number of nanobots that are in range of it, including itself.

For example, given the following nanobots:

pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1

The strongest nanobot is the first one (position 0,0,0) because its signal radius, 4 is the largest. Using that nanobot's location and signal radius, the following nanobots are in or out of range:

    The nanobot at 0,0,0 is distance 0 away, and so it is in range.
    The nanobot at 1,0,0 is distance 1 away, and so it is in range.
    The nanobot at 4,0,0 is distance 4 away, and so it is in range.
    The nanobot at 0,2,0 is distance 2 away, and so it is in range.
    The nanobot at 0,5,0 is distance 5 away, and so it is not in range.
    The nanobot at 0,0,3 is distance 3 away, and so it is in range.
    The nanobot at 1,1,1 is distance 3 away, and so it is in range.
    The nanobot at 1,1,2 is distance 4 away, and so it is in range.
    The nanobot at 1,3,1 is distance 5 away, and so it is not in range.

In this example, in total, 7 nanobots are in range of the nanobot with the largest signal radius.

Find the nanobot with the largest signal radius. How many nanobots are in range of its signals?

--- Part Two ---

Now, you just need to figure out where to position yourself so that you're actually teleported when the nanobots activate.

To increase the probability of success, you need to find the coordinate which puts you in range of the largest number of nanobots. If there are multiple, choose one closest to your position (0,0,0, measured by manhattan distance).

For example, given the following nanobot formation:

pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5

Many coordinates are in range of some of the nanobots in this formation. However, only the coordinate 12,12,12 is in range of the most nanobots: it is in range of the first five, but is not in range of the nanobot at 10,10,10. (All other coordinates are in range of fewer than five nanobots.) This coordinate's distance from 0,0,0 is 36.

Find the coordinates that are in range of the largest number of nanobots. What is the shortest manhattan distance between any of those points and 0,0,0?
"""

import re

import z3


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def z_manhattan1(a, b):
    d = a - b
    return z3.If(d >= 0, d, -d)


def z_manhattan3(a, b):
    return (
        z_manhattan1(a[0], b[0]) + z_manhattan1(a[1], b[1]) + z_manhattan1(a[2], b[2])
    )


def in_range(a, b):
    """
    Check if b is in range of a.
    """
    if manhattan(a, b) <= a[3]:
        return True
    else:
        return False


if __name__ == "__main__":
    # Read input.
    bots = []
    with open("input", "r") as file:
        for line in file:
            match = re.match("pos=<([\-0-9]+),([\-0-9]+),([\-0-9]+)>, r=([0-9]+)", line)
            if match:
                bot = [match.group(1), match.group(2), match.group(3), match.group(4)]
                bot = tuple([int(x) for x in bot])
                bots.append(bot)

    # Find the strongest bot.
    biggest_v = 0
    biggest_i = -1
    for i, bot in enumerate(bots):
        if bot[3] > biggest_v:
            biggest_v = bot[3]
            biggest_i = i

    # Find what is in range.
    cnt = 0
    for i, bot in enumerate(bots):
        if in_range(bots[biggest_i], bot):
            cnt += 1

    print(f"Answer 1 is {cnt}.")

    # Part 2 is tough, because the search space is real fucking sparse.
    # Binary search is tempting but not guaranteed to work the way I see others implement.
    solver = z3.Optimize()

    x_ans = z3.Int("x_ans")
    y_ans = z3.Int("y_ans")
    z_ans = z3.Int("z_ans")
    dist_ans = z3.Int("dist_ans")

    inside = []
    for i, bot in enumerate(bots):
        bot_no = z3.Int("b{:4d}".format(i))
        ok = z3.If(
            z_manhattan3([x_ans, y_ans, z_ans], [bot[0], bot[1], bot[2]]) <= bot[3],
            1,
            0,
        )
        solver.add(bot_no == ok)
        inside.append(bot_no)

    solver.add(dist_ans == z_manhattan3([x_ans, y_ans, z_ans], [0, 0, 0]))

    solver.maximize(z3.Sum(*inside))
    solver.minimize(dist_ans)
    solver.check()

    m = solver.model()
    min_distance = m.eval(dist_ans)
    print(f"Answer 2 is {min_distance}.")
