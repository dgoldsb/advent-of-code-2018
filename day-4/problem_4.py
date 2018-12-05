"""
The polymer is formed by smaller units which, when triggered, react with each other such that two adjacent units of the same type and opposite polarity are destroyed. Units' types are represented by letters; units' polarity is represented by capitalization. For instance, r and R are units with the same type but opposite polarity, whereas r and s are entirely different types and do not react.

For example:

    In aA, a and A react, leaving nothing behind.
    In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
    In abAB, no two adjacent units are of the same type, and so nothing happens.
    In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.

Now, consider a larger example, dabAcCaCBAcCcaDA:

dabAcCaCBAcCcaDA  The first 'cC' is removed.
dabAaCBAcCcaDA    This creates 'Aa', which is removed.
dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
dabCBAcaDA        No further actions can be taken.

After all possible reactions, the resulting polymer contains 10 units.

How many units remain after fully reacting the polymer you scanned?

--- Part Two ---

Time to improve the polymer.

One of the unit types is causing problems; it's preventing the polymer from collapsing as much as it should. Your goal is to figure out which unit type is causing the most problems, remove all instances of it (regardless of polarity), fully react the remaining polymer, and measure its length.

For example, again using the polymer dabAcCaCBAcCcaDA from above:

    Removing all A/a units produces dbcCCBcCcD. Fully reacting this polymer produces dbCBcD, which has length 6.
    Removing all B/b units produces daAcCaCAcCcaDA. Fully reacting this polymer produces daCAcaDA, which has length 8.
    Removing all C/c units produces dabAaBAaDA. Fully reacting this polymer produces daDA, which has length 4.
    Removing all D/d units produces abAcCaCBAcCcaA. Fully reacting this polymer produces abCBAc, which has length 6.

In this example, removing all C/c units was best, producing the answer 4.

What is the length of the shortest polymer you can produce by removing all units of exactly one type and fully reacting the result?
"""

from copy import copy
import sys


# Check for pair.
def check_pair(x, y):
    if (x.lower() == y and x == y.upper()) or (x.upper() == y and x == y.lower()):
        return True
    else:
        return False


# Do a recursive substitution.
def substitute_pair(polymer):
    # Count the number of substitutions.
    indices = set()

    found_previous = False
    for i1 in range(1, len(polymer)):
        if found_previous:
            found_previous = False
            continue
        i0 = i1 - 1
        if check_pair(polymer[i0], polymer[i1]):
            indices.add(i0)
            indices.add(i1)
            found_previous = True
        else:
            found_previous = False

    # Recurse or return.
    if len(list(indices)) > 0:
        list_indices = list(indices)
        list_indices.sort()
        for index in list_indices[::-1]:
            del polymer[index]
        return substitute_pair(polymer)
    else:
        return polymer


if __name__ == '__main__':
    # Read the input string.
    with open('input', 'r') as file:
        input = list(file.read().replace('\n', ''))
    sys.setrecursionlimit(10000)

    # Get the result.
    result = substitute_pair(input)
    print(f'Answer 1 is {len(result)}')

    # Get the set of all elements.
    elements = set([x.lower() for x in input])

    shortest = len(input)
    for element in list(elements):
        print(f'Testing element {element}')
        edited_input = copy(input)
        edited_input = [x for x in edited_input if x not in [element.lower(), element.upper()]]
        length_polymer = len(substitute_pair(edited_input))
        if length_polymer < shortest:
            shortest = length_polymer
    print(f'Answer 2 is {shortest}.')
