"""
You map out the tracks (your puzzle input) and see where you can help.

Tracks consist of straight paths (| and -), curves (/ and \), and intersections (+). Curves connect exactly two perpendicular pieces of track; for example, this is a closed loop:

/----\
|    |
|    |
\----/

Intersections occur when two perpendicular paths cross. At an intersection, a cart is capable of turning left, turning right, or continuing straight. Here are two loops connected by two intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/

Several carts are also on the tracks. Carts always face either up (^), down (v), left (<), or right (>). (On your initial map, the track under each cart is a straight path matching the direction the cart is facing.)

Each time a cart has the option to turn (by arriving at any intersection), it turns left the first time, goes straight the second time, turns right the third time, and then repeats those directions starting again with left the fourth time, straight the fifth time, and so on. This process is independent of the particular intersection at which the cart has arrived - that is, the cart has no per-intersection memory.

Carts all move at the same speed; they take turns moving a single step at a time. They do this based on their current location: carts on the top row move first (acting from left to right), then carts on the second row move (again from left to right), then carts on the third row, and so on. Once each cart has moved one step, the process repeats; each of these loops is called a tick.

After following their respective paths for a while, the carts eventually crash. To help prevent crashes, you'd like to know the location of the first crash. Locations are given in X,Y coordinates, where the furthest left column is X=0 and the furthest top row is Y=0.
"""

import sys

DIRS = ['^', '>', 'v', '<']


class Cart:
    def __init__(self, dir):
        self.dir = dir
        self.dir_to_vel()
        self.next_turn = 'left'

    def bend(self, c):
        if c == '\\' and self.dir == '^':
            self.dir = '<'
        elif c == '\\' and self.dir == '>':
            self.dir = 'v'
        elif c == '\\' and self.dir == '<':
            self.dir = '^'
        elif c == '\\' and self.dir == 'v':
            self.dir = '>'
        elif c == '/' and self.dir == '^':
            self.dir = '>'
        elif c == '/' and self.dir == '>':
            self.dir = '^'
        elif c == '/' and self.dir == '<':
            self.dir = 'v'
        elif c == '/' and self.dir == 'v':
            self.dir = '<'

        self.dir_to_vel()

    def dir_to_vel(self):
        if self.dir == '^':
            self.vel = [-1, 0]
        elif self.dir == '>':
            self.vel = [0, 1]
        elif self.dir == 'v':
            self.vel = [1, 0]
        elif self.dir == '<':
            self.vel = [0, -1]
        else:
            raise ValueError('Unknown direction')

    def step(self, coords):
        return [x + dx for x, dx in zip(coords, self.vel)]

    def turn(self):
        curr_index = DIRS.index(self.dir)
        if self.next_turn == 'left':
            curr_index = ((curr_index - 1) + 4) % 4
            self.next_turn = 'straight'
        elif self.next_turn == 'right':
            curr_index = (curr_index + 1) % 4
            self.next_turn = 'left'
        else:
            self.next_turn = 'right'

        self.dir = DIRS[curr_index]
        self.dir_to_vel()


if __name__ == '__main__':
    # Read input.
    grid = []
    with open('input', 'r') as file:
        for line in file.readlines():
            # We create a double layer, one for carts, one for tracks.
            grid.append([[x, None] for x in list(line)])

    # Move carts to the right layer.
    for row in grid:
        for cell in row:
            if cell[0] in DIRS:
                cell[1] = Cart(cell[0])
                if cell[0] in ['<', '>']:
                    cell[0] = '-'
                else:
                    cell[0] = '|'

    # Do ticks.
    iter = 0
    while True:
        print(f'tick {iter}')
        iter += 1
        moves = []

        already_moved = []

        for x, row in enumerate(grid):
            for y, cell in enumerate(row):
                if (x, y) in already_moved:
                    pass
                elif isinstance(cell[1], Cart):
                    if cell[0] == '+':
                        cell[1].turn()
                    elif cell[0] in ['/', '\\']:
                        cell[1].bend(cell[0])

                    new_coords = cell[1].step([x, y])
                    new_x = new_coords[0]
                    new_y = new_coords[1]

                    if isinstance(grid[new_x][new_y][1], Cart):
                        print(f'Answer 1 is {new_y},{new_x}.')
                        sys.exit(0)
                    else:
                        print([x, y])
                        print([new_x, new_y])
                        grid[new_x][new_y][1] = cell[1]
                        cell[1] = None
                        already_moved.append((new_x, new_y))
