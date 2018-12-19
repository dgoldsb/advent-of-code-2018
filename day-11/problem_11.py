"""
After exploring a little, you discover a long tunnel that contains a row of small pots as far as you can see to your left and right. A few of them contain plants - someone is trying to grow things in these geothermally-heated caves.

The pots are numbered, with 0 in front of you. To the left, the pots are numbered -1, -2, -3, and so on; to the right, 1, 2, 3.... Your puzzle input contains a list of pots from 0 to the right and whether they do (#) or do not (.) currently contain a plant, the initial state. (No other pots currently contain plants.) For example, an initial state of #..##.... indicates that pots 0, 3, and 4 currently contain plants.

Your puzzle input also contains some notes you find on a nearby table: someone has been trying to figure out how these plants spread to nearby pots. Based on the notes, for each generation of plants, a given pot has or does not have a plant based on whether that pot (and the two pots on either side of it) had a plant in the last generation. These are written as LLCRR => N, where L are pots to the left, C is the current pot being considered, R are the pots to the right, and N is whether the current pot will have a plant in the next generation. For example:

    A note like ..#.. => . means that a pot that contains a plant but with no plants within two pots of it will not have a plant in it during the next generation.
    A note like ##.## => . means that an empty pot with two plants on each side of it will remain empty in the next generation.
    A note like .##.# => # means that a pot has a plant in a given generation if, in the previous generation, there were plants in that pot, the one immediately to the left, and the one two pots to the right, but not in the ones immediately to the right and two to the left.

It's not clear what these plants are for, but you're sure it's important, so you'd like to make sure the current configuration of plants is sustainable by determining what will happen after 20 generations.

For example, given the following input:

initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #

For brevity, in this example, only the combinations which do produce a plant are listed. (Your input includes all possible combinations.) Then, the next 20 generations will look like this:

                 1         2         3
       0         0         0         0
 0: ...#..#.#..##......###...###...........
 1: ...#...#....#.....#..#..#..#...........
 2: ...##..##...##....#..#..#..##..........
 3: ..#.#...#..#.#....#..#..#...#..........
 4: ...#.#..#...#.#...#..#..##..##.........
 5: ....#...##...#.#..#..#...#...#.........
 6: ....##.#.#....#...#..##..##..##........
 7: ...#..###.#...##..#...#...#...#........
 8: ...#....##.#.#.#..##..##..##..##.......
 9: ...##..#..#####....#...#...#...#.......
10: ..#.#..#...#.##....##..##..##..##......
11: ...#...##...#.#...#.#...#...#...#......
12: ...##.#.#....#.#...#.#..##..##..##.....
13: ..#..###.#....#.#...#....#...#...#.....
14: ..#....##.#....#.#..##...##..##..##....
15: ..##..#..#.#....#....#..#.#...#...#....
16: .#.#..#...#.#...##...#...#.#..##..##...
17: ..#...##...#.#.#.#...##...#....#...#...
18: ..##.#.#....#####.#.#.#...##...##..##..
19: .#..###.#..#.#.#######.#.#.#..#.#...#..
20: .#....##....#####...#######....#.#..##.

The generation is shown along the left, where 0 is the initial state. The pot numbers are shown along the top, where 0 labels the center pot, negative-numbered pots extend to the left, and positive pots extend toward the right. Remember, the initial state begins at pot 0, which is not the leftmost pot used in this example.

After one generation, only seven plants remain. The one in pot 0 matched the rule looking for ..#.., the one in pot 4 matched the rule looking for .#.#., pot 9 matched .##.., and so on.

In this example, after 20 generations, the pots shown as # contain plants, the furthest left of which is pot -2, and the furthest right of which is pot 34. Adding up all the numbers of plant-containing pots after the 20th generation produces 325.

After 20 generations, what is the sum of the numbers of all pots which contain a plant?
"""

import re

GENERATIONS = 50000000000


class Pot():
    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.previous_value = value
        self.left = None
        self.right = None

    def timestep(self, dictionary):
        # Create pots if required.
        if self.left is None:
            self.left = Pot(self.index - 1, '.')
            self.left.right = self
        if self.left.left is None:
            self.left.left = Pot(self.index - 2, '.')
            self.left.left.right = self.left
        if self.right is None:
            self.right = Pot(self.index + 1, '.')
            self.right.left = self
        if self.right.right is None:
            self.right.right = Pot(self.index + 2, '.')
            self.right.right.left = self.right

        # Find and set the next value.
        key = (self.left.left.previous_value, self.left.previous_value,
               self.value, self.right.value, self.right.right.value)
        self.previous_value = self.value
        try:
            self.value = dictionary[key]
        except:
            self.value = '.'


def prune_pots(first, last):
    while first.right.value == '.' and first.right.right == '.' and first.value == '.':
        first = first.right
        del first.left
        first.left = None

    while first.right.value == '.' and first.right.right == '.' and first.value == '.':
        first = first.right
        del first.left
        first.left = None

    return first, last


def score(current_pot):
    total = 0
    while True:
        if current_pot.value == '#':
            total += current_pot.index

        if current_pot.right is None:
            break
        else:
            current_pot = current_pot.right
    return total


if __name__ == '__main__':
    first_pot = None
    last_pot = None
    pots = []
    dictionary = dict()

    # Read input.
    with open('input', 'r') as file:
        for line in file.readlines():
            matches = re.findall('[\.#]+', line)

            if matches and line[0] == 'i':
                initial_state = list(matches[0])
                for index, value in enumerate(initial_state):
                    pots.append(Pot(index, value))
                    if index != 0:
                        pots[-1].left = pots[-2]
                        pots[-2].right = pots[-1]
                first_pot = pots[0]
                last_pot = pots[-1]
            elif matches:
                key = tuple(list(matches[0]))
                value = matches[1]
                dictionary[key] = value

    # Do timesteps
    total = 0
    last_df = 0
    stability = 0
    for index in range(GENERATIONS):
        # Create two pots to the right.
        for _ in range(2):
            last_pot.right = Pot(last_pot.index + 1, '.')
            last_pot.right.left = last_pot
            last_pot = last_pot.right

        # Create two pots to the left.
        for _ in range(2):
            first_pot.left = Pot(first_pot.index - 1, '.')
            first_pot.left.right = first_pot
            first_pot = first_pot.left

        current_pot = first_pot
        pots_to_update = []

        while True:
            pots_to_update.append(current_pot)
            if current_pot.right is None:
                break
            else:
                current_pot = current_pot.right


        for pot in pots_to_update:
            pot.timestep(dictionary)

        # Print the state.
        first_pot = first_pot.left.left
        last_pot = last_pot.right.right
        first_pot, last_pot = prune_pots(first_pot, last_pot)

        new_total = score(first_pot)
        df = new_total - total
        total = new_total

        if df == last_df:
            stability += 1
        else:
            last_df = df

        if stability == 10:
            print(index)
            total += (GENERATIONS - index - 1) * df
            break

    print(f'Answer is {total}.')
