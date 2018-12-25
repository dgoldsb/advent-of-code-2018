"""
The cave is divided into square regions which are either dominantly rocky, narrow, or wet (called its type). Each region occupies exactly one coordinate in X,Y format where X and Y are integers and zero or greater. (Adjacent regions can be the same type.)

The scan (your puzzle input) is not very detailed: it only reveals the depth of the cave system and the coordinates of the target. However, it does not reveal the type of each region. The mouth of the cave is at 0,0.

The man explains that due to the unusual geology in the area, there is a method to determine any region's type based on its erosion level. The erosion level of a region can be determined from its geologic index. The geologic index can be determined using the first rule that applies from the list below:

    The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    The region at the coordinates of the target has a geologic index of 0.
    If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
    If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
    Otherwise, the region's geologic index is the result of multiplying the erosion levels of the regions at X-1,Y and X,Y-1.

A region's erosion level is its geologic index plus the cave system's depth, all modulo 20183. Then:

    If the erosion level modulo 3 is 0, the region's type is rocky.
    If the erosion level modulo 3 is 1, the region's type is wet.
    If the erosion level modulo 3 is 2, the region's type is narrow.

For example, suppose the cave system's depth is 510 and the target's coordinates are 10,10. Using % to represent the modulo operator, the cavern would look as follows:

    At 0,0, the geologic index is 0. The erosion level is (0 + 510) % 20183 = 510. The type is 510 % 3 = 0, rocky.
    At 1,0, because the Y coordinate is 0, the geologic index is 1 * 16807 = 16807. The erosion level is (16807 + 510) % 20183 = 17317. The type is 17317 % 3 = 1, wet.
    At 0,1, because the X coordinate is 0, the geologic index is 1 * 48271 = 48271. The erosion level is (48271 + 510) % 20183 = 8415. The type is 8415 % 3 = 0, rocky.
    At 1,1, neither coordinate is 0 and it is not the coordinate of the target, so the geologic index is the erosion level of 0,1 (8415) times the erosion level of 1,0 (17317), 8415 * 17317 = 145722555. The erosion level is (145722555 + 510) % 20183 = 1805. The type is 1805 % 3 = 2, narrow.
    At 10,10, because they are the target's coordinates, the geologic index is 0. The erosion level is (0 + 510) % 20183 = 510. The type is 510 % 3 = 0, rocky.

Drawing this same cave system with rocky as ., wet as =, narrow as |, the mouth as M, the target as T, with 0,0 in the top-left corner, X increasing to the right, and Y increasing downward, the top-left corner of the map looks like this:

M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Before you go in, you should determine the risk level of the area. For the the rectangle that has a top-left corner of region 0,0 and a bottom-right corner of the region containing the target, add up the risk level of each individual region: 0 for rocky regions, 1 for wet regions, and 2 for narrow regions.

In the cave system above, because the mouth is at 0,0 and the target is at 10,10, adding up the risk level of all regions with an X coordinate from 0 to 10 and a Y coordinate from 0 to 10, this total is 114.

What is the total risk level for the smallest rectangle that includes 0,0 and the target's coordinates?

--- Part Two ---

Okay, it's time to go rescue the man's friend.

As you leave, he hands you some tools: a torch and some climbing gear. You can't equip both tools at once, but you can choose to use neither.

Tools can only be used in certain regions:

    In rocky regions, you can use the climbing gear or the torch. You cannot use neither (you'll likely slip and fall).
    In wet regions, you can use the climbing gear or neither tool. You cannot use the torch (if it gets wet, you won't have a light source).
    In narrow regions, you can use the torch or neither tool. You cannot use the climbing gear (it's too bulky to fit).

You start at 0,0 (the mouth of the cave) with the torch equipped and must reach the target coordinates as quickly as possible. The regions with negative X or Y are solid rock and cannot be traversed. The fastest route might involve entering regions beyond the X or Y coordinate of the target.

You can move to an adjacent region (up, down, left, or right; never diagonally) if your currently equipped tool allows you to enter that region. Moving to an adjacent region takes one minute. (For example, if you have the torch equipped, you can move between rocky and narrow regions, but cannot enter wet regions.)

You can change your currently equipped tool or put both away if your new equipment would be valid for your current region. Switching to using the climbing gear, torch, or neither always takes seven minutes, regardless of which tools you start with. (For example, if you are in a rocky region, you can switch from the torch to the climbing gear, but you cannot switch to neither.)

Finally, once you reach the target, you need the torch equipped before you can find him in the dark. The target is always in a rocky region, so if you arrive there with climbing gear equipped, you will need to spend seven minutes switching to your torch.

This is tied with other routes as the fastest way to reach the target: 45 minutes. In it, 21 minutes are spent switching tools (three times, seven minutes each) and the remaining 24 minutes are spent moving.

What is the fewest number of minutes you can take to reach the target?
"""

from collections import defaultdict
import heapq
import numpy as np
import re


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.weights = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = distance

    def neighbors(self, current):
        return self.edges[current]

    def cost(self, current, next):
        return self.weights[(current, next)]


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def heuristic(a, b):
    (x1, y1, z1) = a
    (x2, y2, z2) = b
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


if __name__ == '__main__':
    # Read input.
    with open('example', 'r') as file:
        body = file.read()
        depth = int(re.search('depth: ([0-9]+)', body).group(1))
        match = re.search('target: ([0-9]+),([0-9]+)', body)
        xt = int(match.group(1))
        yt = int(match.group(2))

    def geo_to_ero(a):
        return (a + depth) % 20183

    # Create the grid.
    geo_index = np.empty(shape=(xt+1, yt+1))
    total_risk_level = 0

    for x in range(xt+1):
        for y in range(yt+1):
            if (x == 0 and y == 0) or(x == xt and y == yt):
                geo_index[x][y] = 0
            elif y == 0:
                geo_index[x][y] = x * 16807
            elif x == 0:
                geo_index[x][y] = y * 48271
            else:
                geo_index[x][y] = geo_to_ero(geo_index[x-1][y]) * \
                                  geo_to_ero(geo_index[x][y-1])

            total_risk_level += int(geo_to_ero(geo_index[x][y]) % 3)

    print(f'Answer 1 is {total_risk_level}')

    # We need a bigger grid, let's make a safety margin.
    big_grid = np.empty(shape=(xt+50, yt+50))
    for x in range(xt+50):
        for y in range(yt+50):
            if (x == 0 and y == 0) or (x == xt and y == yt):
                big_grid[x][y] = 0
            elif y == 0:
                big_grid[x][y] = x * 16807
            elif x == 0:
                big_grid[x][y] = y * 48271
            else:
                big_grid[x][y] = geo_to_ero(big_grid[x-1][y]) * geo_to_ero(big_grid[x][y-1])

    def geo_to_type(a):
        return geo_to_ero(a) % 3

    # Construct the graph.
    graph = Graph()
    for x in range(xt+50):
        for y in range(yt+50):
            terrain = geo_to_type(big_grid[x][y])

            for state in [0, 1, 2]:  # 0 none, 1 climbing gear, 2 flashlight
                if (terrain != state) or terrain == 0:
                    # Create a node.
                    node = (x, y, state)
                    graph.add_node(node)

                    # Now to create some fucking edges.
                    for xdt in [-1, 1]:
                        if x + xdt == -1 or x + xdt == xt + 50:
                            continue
                        for ydt in [-1, 1]:
                            if y + ydt == -1 or y + ydt == yt + 50:
                                continue

                            terrain_next = geo_to_type(big_grid[x + xdt][y + ydt])
                            if (terrain_next != state) or terrain_next == 0:
                                node_next = (x + xdt, y + ydt, state)
                                graph.add_node(node_next)
                                graph.add_edge(node, node_next, 1)

                    # Also we can switch our fucking gear.
                    for state_next in [0, 1, 2]:
                        if ((terrain != state_next) or terrain == 0) and state != state_next:
                            node_next = (x, y, state_next)
                            graph.add_edge(node, node_next, 7)

    start, cost_so_far = a_star_search(graph, (0, 0, 1), (xt, yt, 1))
    print(f'Answer 2 is {cost_so_far[(xt, yt, 1)]}.')
