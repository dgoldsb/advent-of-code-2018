"""
On the outskirts of the North Pole base construction project, many Elves are collecting lumber.

The lumber collection area is 50 acres by 50 acres; each acre can be either open ground (.), trees (|), or a lumberyard (#). You take a scan of the area (your puzzle input).

Strange magic is at work here: each minute, the landscape looks entirely different. In exactly one minute, an open acre can fill with trees, a wooded acre can be converted to a lumberyard, or a lumberyard can be cleared to open ground (the lumber having been sent to other projects).

The change to each acre is based entirely on the contents of that acre as well as the number of open, wooded, or lumberyard acres adjacent to it at the start of each minute. Here, "adjacent" means any of the eight acres surrounding that acre. (Acres on the edges of the lumber collection area might have fewer than eight adjacent acres; the missing acres aren't counted.)

In particular:

    An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
    An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
    An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.

These changes happen across all acres simultaneously, each of them using the state of all acres at the beginning of the minute and changing to their new form by the end of that same minute. Changes that happen during the minute don't affect each other.
"""
from typing import Generator, Sequence


def detect_cycle(sequence: Sequence[int]) -> tuple[int, int]:
    """Detects a cycle in a sequence."""
    seen = {}
    for i, item in enumerate(sequence):
        if item in seen:
            return seen[item], i
        seen[item] = i
    return 0, 0


def adjacent_slots(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    for x_ in [x - 1, x, x + 1]:
        for y_ in [y - 1, y, y + 1]:
            if x == x_ and y == y_:
                continue
            yield x_, y_


def parse_input(
    input_: str,
) -> tuple[set[tuple[int, int]], set[tuple[int, int]], set[tuple[int, int]]]:
    trees = set()
    lumberyards = set()
    open_ground = set()
    for x, line in enumerate(input_.splitlines()):
        for y, c in enumerate(line):
            match c:
                case ".":
                    open_ground.add((x, y))
                case "|":
                    trees.add((x, y))
                case "#":
                    lumberyards.add((x, y))
    return trees, lumberyards, open_ground


def solve(
    trees: set[tuple[int, int]],
    lumberyards: set[tuple[int, int]],
    open_ground: set[tuple[int, int]],
    minutes: int,
) -> int:
    """Solution to part one."""
    states = []
    state_values = {}

    for minute in range(minutes):
        new_trees = set()
        new_lumberyards = set()
        new_open_ground = set()

        for tree in trees:
            adjacent_slots_with_lumberyards = len(
                set(adjacent_slots(*tree)).intersection(lumberyards)
            )
            if adjacent_slots_with_lumberyards >= 3:
                new_lumberyards.add(tree)
            else:
                new_trees.add(tree)

        for lumberyard in lumberyards:
            adjacent_slots_with_lumberyards = len(
                set(adjacent_slots(*lumberyard)).intersection(lumberyards)
            )
            adjacent_slots_with_trees = len(
                set(adjacent_slots(*lumberyard)).intersection(trees)
            )
            if adjacent_slots_with_lumberyards > 0 and adjacent_slots_with_trees > 0:
                new_lumberyards.add(lumberyard)
            else:
                new_open_ground.add(lumberyard)

        for spot in open_ground:
            adjacent_slots_with_trees = len(
                set(adjacent_slots(*spot)).intersection(trees)
            )
            if adjacent_slots_with_trees >= 3:
                new_trees.add(spot)
            else:
                new_open_ground.add(spot)

        trees = new_trees
        lumberyards = new_lumberyards
        open_ground = new_open_ground

        state = hash(tuple(sorted(trees)) + tuple(sorted(lumberyards)))
        states.append(state)

        if state in state_values:

            def _get_value(index_: int) -> int:
                cycle_start = states.index(state)
                cycle_length = len(states) - cycle_start - 1
                target_in_cycle = (index_ - cycle_start) % cycle_length
                return state_values[states[cycle_start + target_in_cycle]]

            assert _get_value(minute) == state_values[state]
            # 163494 too low 190518 too high, 185885 too high
            return _get_value(minutes)

        state_values[state] = len(trees) * len(lumberyards)

    return state_values[states[-1]]


with open("example") as f:
    example_input = f.read()

parsed_example_inputs = parse_input(example_input)
assert solve(*parsed_example_inputs, minutes=10) == 1147

with open("input") as f:
    input_ = f.read()

parsed_inputs = parse_input(input_)
print(f"A: {solve(*parsed_inputs, minutes=10)}")
print(f"B: {solve(*parsed_inputs, minutes=1_000_000_000)}")
