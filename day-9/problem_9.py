"""
Each line represents one point. Positions are given as <X, Y> pairs: X represents how far left (negative) or right (positive) the point appears, while Y represents how far up (negative) or down (positive) the point appears.

At 0 seconds, each point has the position given. Each second, each point's velocity is added to its position. So, a point with velocity <1, -2> is moving to the right, but is moving upward twice as quickly. If this point's initial position were <3, 9>, after 3 seconds, its position would become <6, 3>.

After 3 seconds, the message appeared briefly: HI. Of course, your message will be much longer and will take many more seconds to appear.

What message will eventually appear in the sky

--- Part Two ---

Good thing you didn't have to wait, because that would have taken a long time - much longer than the 3 seconds in the example above.

Impressed by your sub-hour communication capabilities, the Elves are curious: exactly how many seconds would they have needed to wait for that message to appear?

"""

import re

def print_lights(lights):
    min_x = min([light.x for light in lights])
    min_y = min([light.y for light in lights])

    for light in lights:
        light.x -= min_x
        light.y -= min_y

    max_x = max([light.x for light in lights])
    max_y = max([light.y for light in lights])
    grid = []
    for y in range(max_y + 1):
        line = []
        for x in range(max_x + 1):
            line.append('.')
        grid.append(line)

    for light in lights:
        grid[light.y][light.x] = '#'

    print('\n'.join([''.join(x) for x in grid]))


class Light:
    def __init__(self, x, y, xv, yv):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv

    def timestep(self):
        self.x += self.xv
        self.y += self.yv


if __name__ == '__main__':
    # Read input.
    with open('input', 'r') as file:
        lights = []
        for line in file.readlines():
            matches = re.findall('[0-9\-]+', line)
            if matches:
                lights.append(Light(int(matches[0]), int(matches[1]),
                                    int(matches[2]), int(matches[3])))


    counter = 0
    was_not_in_scope = True
    in_scope = False
    while was_not_in_scope or in_scope:
        for light in lights:
            light.timestep()
        counter += 1

        in_scope = abs(min([light.x for light in lights]) - max([light.x for light in lights])) < 100

        if in_scope:
            was_not_in_scope = False
            print(f'You waited {counter} seconds...')
            print_lights(lights)
