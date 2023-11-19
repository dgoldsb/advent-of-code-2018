"""
After feeling like you've been falling for a few minutes, you look at the device's tiny screen. "Error: Device must be calibrated before first use. Frequency drift detected. Cannot maintain destination lock." Below the message, the device shows a sequence of changes in frequency (your puzzle input). A value like +6 means the current frequency increases by 6; a value like -3 means the current frequency decreases by 3.

For example, if the device displays frequency changes of +1, -2, +3, +1, then starting from a frequency of zero, the following changes would occur:

    Current frequency  0, change of +1; resulting frequency  1.
    Current frequency  1, change of -2; resulting frequency -1.
    Current frequency -1, change of +3; resulting frequency  2.
    Current frequency  2, change of +1; resulting frequency  3.

In this example, the resulting frequency is 3.

Here are other example situations:

    +1, +1, +1 results in  3
    +1, +1, -2 results in  0
    -1, -2, -3 results in -6

Starting with a frequency of zero, what is the resulting frequency after all of the changes in frequency have been applied?

--- Part Two ---

You notice that the device repeats the same frequency change list over and over. To calibrate the device, you need to find the first frequency it reaches twice.
What is the first frequency your device reaches twice?
"""

if __name__ == "__main__":
    # Part 1.
    values = []
    with open("input", "r") as file:
        for row in file:
            values.append(int(row))
    print("Answer 1 is {}".format(sum(values)))

    iterations = 0
    total = 0
    visited_values = set()
    visited_values.add(total)
    found = False
    while not found:
        for value in values:
            total += value
            if total in visited_values:
                print("Answer 2 is {}".format(total))
                found = True
                break
            visited_values.add(total)
        iterations += 1
        print("{} iterations done".format(iterations))
