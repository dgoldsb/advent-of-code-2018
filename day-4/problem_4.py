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
"""

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
    print(f'Entering recurse with length {len(polymer)}')
    indices = set()

    for i1 in range(1, len(polymer)):
        i0 = i1 - 1
        if check_pair(polymer[i0], polymer[i1]):
            indices.add(i0)
            indices.add(i1)

    # Recurse or return.
    if len(list(indices)) > 0:
        list_indices = list(indices)
        list_indices.sort()
        for index in list_indices[::-1]:
            print(index)
            del polymer[index]
        return substitute_pair(polymer)
    else:
        return polymer


if __name__ == '__main__':
    # Read the input string.
    with open('input', 'r') as file:
        input = list(file.read().replace('\n', ''))

    # Get the result.
    result = substitute_pair(input)
    print(result[:10])
    print(result[-10:])
    print(f'Answer 1 is {len(result)}')
