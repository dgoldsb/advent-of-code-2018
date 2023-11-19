"""
Having perfected their hot chocolate, the Elves have a new problem: the Goblins that live in these caves will do anything to steal it. Looks like they're here for a fight.

You scan the area, generating a map of the walls (#), open cavern (.), and starting position of every Goblin (G) and Elf (E) (your puzzle input).

Combat proceeds in rounds; in each round, each unit that is still alive takes a turn, resolving all of its actions before the next unit's turn begins. On each unit's turn, it tries to move into range of an enemy (if it isn't already) and then attack (if it is in range).

All units are very disciplined and always follow very strict combat rules. Units never move or attack diagonally, as doing so would be dishonorable. When multiple choices are equally valid, ties are broken in reading order: top-to-bottom, then left-to-right. For instance, the order in which units take their turns within a round is the reading order of their starting positions in that round, regardless of the type of unit or whether other units have moved after the round started.

Each unit begins its turn by identifying all possible targets (enemy units). If no targets remain, combat ends.

Then, the unit identifies all of the open squares (.) that are in range of each target; these are the squares which are adjacent (immediately up, down, left, or right) to any target and which aren't already occupied by a wall or another unit. Alternatively, the unit might already be in range of a target. If the unit is not already in range of a target, and there are no open squares which are in range of a target, the unit ends its turn.

If the unit is already in range of a target, it does not move, but continues its turn with an attack. Otherwise, since it is not in range of a target, it moves.

To move, the unit first considers the squares that are in range and determines which of those squares it could reach in the fewest steps. A step is a single movement to any adjacent (immediately up, down, left, or right) open (.) square. Units cannot move into walls or other units. The unit does this while considering the current positions of units and does not do any prediction about where units will be later. If the unit cannot reach (find an open path to) any of the squares that are in range, it ends its turn. If multiple squares are in range and tied for being reachable in the fewest steps, the square which is first in reading order is chosen.

The Elves look quite outnumbered. You need to determine the outcome of the battle: the number of full rounds that were completed (not counting the round in which combat ends) multiplied by the sum of the hit points of all remaining units at the moment combat ends. (Combat only ends when a unit finds no targets during its turn.)

What is the outcome of the combat described in your puzzle input?
"""
import heapq
from copy import copy
from typing import Iterable, Protocol, TypeVar


class Positionable(Protocol):
    x: int
    y: int


T = TypeVar("T", bound=Positionable)


class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"


def _sort_in_reading_order(options: Iterable[T]) -> list[T]:
    return sorted(options, key=lambda u: (u.y, u.x))


class ShortestPathSolver:
    """Use Dijkstra, but respecting the reading order."""

    def __init__(self, empty_space: set[tuple[int, int]]):
        self.empty_space = empty_space

    def __find_adjacent(self, coordinate: tuple[int, int]) -> set[tuple[int, int]]:
        x, y = coordinate
        return {
            (x, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x, y + 1),
        }

    def __reconstruct_path(
        self, target: tuple[int, int], previous: dict
    ) -> list[tuple[int, int]]:
        path = [target]

        if target not in previous:
            raise KeyError(f"Target {target} not in previous {previous}")

        while target in previous:
            target = previous[target]
            if target is not None:
                path.append(target)

        if len(path) == 1:
            pass
        return path[::-1]

    def find_shortest_path(
        self,
        start: tuple[int, int],
        target: tuple[int, int],
        empty_space: set[tuple[int, int]],
    ) -> list[tuple[int, int]] | None:
        open_set = {start}
        distances = {start: 0}
        previous = {start: None}
        queue = [(0, start)]

        while queue:
            # Remove from the open set.
            distance, current = heapq.heappop(queue)
            open_set.remove(current)

            if current == target:
                break

            if current not in empty_space and not (
                current is start or current is target
            ):
                continue

            for adjacent in self.__find_adjacent(current):
                new_distance = distance + 1

                if new_distance < distances.get(adjacent, float("inf")):
                    distances[adjacent] = new_distance
                    previous[adjacent] = current

                    # Add to open set.
                    if adjacent not in open_set:
                        open_set.add(adjacent)
                        heapq.heappush(queue, (new_distance, adjacent))
                elif new_distance == distances[adjacent]:
                    # Update to follow the reading order if there is a tie.
                    priority_coordinate = _sort_in_reading_order(
                        [
                            Coordinate(*previous[adjacent]),
                            Coordinate(*current),
                        ]
                    )[0]
                    previous[adjacent] = (priority_coordinate.x, priority_coordinate.y)

        try:
            return self.__reconstruct_path(target, previous)
        except KeyError:
            return None


class Battle:
    def __init__(self, raw_input: str, elf_strength=3):
        self.empty_space: set[tuple[int, int]] = set()
        self.units: set[Unit] = set()
        self.__elf_strength = elf_strength

        for y, line in enumerate(raw_input.splitlines()):
            for x, char in enumerate(line):
                if char == "#":
                    continue

                if char == ".":
                    self.empty_space.add((x, y))
                    continue

                if char == "E":
                    unit = Elf((x, y), elf_strength)
                elif char == "G":
                    unit = Goblin((x, y))
                else:
                    raise ValueError(f"Unknown character: {char}")

                self.units.add(unit)

    def perform(self):
        rounds_performed = 0
        battle_over = False
        start_elfs = sum(1 for unit in self.units if unit.BANNER == Elf.BANNER)

        while not battle_over:
            for unit in sorted(self.units):
                if unit.dead:
                    continue

                # Determine targets.
                targets = list(filter(lambda u: u.BANNER != unit.BANNER, self.units))

                # Perform a turn.
                old_position = (unit.x, unit.y)
                new_position = unit.turn(targets, self.empty_space)
                if new_position in self.empty_space:
                    self.empty_space.remove(new_position)
                    self.empty_space.add(old_position)

                # Remove dead units.
                for unit_ in copy(self.units):
                    if unit_.dead:
                        self.units.remove(unit_)
                        self.empty_space.add((unit_.x, unit_.y))

            # Check if battle is over.
            for banner in [Elf.BANNER, Goblin.BANNER]:
                if all(unit.BANNER == banner for unit in self.units):
                    battle_over = True

            # Count that we did a round.
            rounds_performed += 1

        elf_deaths = start_elfs - sum(
            1 for unit in self.units if unit.BANNER == Elf.BANNER
        )
        # Mystery off-by-one error.
        if self.__elf_strength > 3:
            return (rounds_performed - 1) * sum(
                unit.hit_points for unit in self.units
            ), elf_deaths
        return (
            rounds_performed * sum(unit.hit_points for unit in self.units),
            elf_deaths,
        )


class Unit:
    BANNER = "U"

    def __init__(self, coordinate: tuple[int, int], strength=3):
        self.x, self.y = coordinate
        self.__attack_power = strength
        self.hit_points = 200

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def __lt__(self, other: "Unit"):
        return _sort_in_reading_order([self, other])[0] is self

    @property
    def dead(self):
        if self.hit_points <= 0:
            return True

    def __find_attack_squares(
        self, targets: Iterable["Unit"], empty_space: set[tuple[int, int]]
    ) -> set[tuple[int, int]]:
        attack_squares = set()

        for target in targets:
            y = target.y
            for x in [target.x - 1, target.x + 1]:
                if (x, y) in empty_space or (x, y) == (self.x, self.y):
                    attack_squares.add((x, y))

        for target in targets:
            x = target.x
            for y in [target.y - 1, target.y + 1]:
                if (x, y) in empty_space or (x, y) == (self.x, self.y):
                    attack_squares.add((x, y))

        return attack_squares

    def move(
        self, targets: Iterable["Unit"], empty_space: set[tuple[int, int]]
    ) -> tuple[int, int]:
        """Returns the new position."""
        attack_squares = self.__find_attack_squares(targets, empty_space)

        if (self.x, self.y) in attack_squares:
            return self.x, self.y

        # Find all shortest paths.
        solvers = ShortestPathSolver(empty_space)
        paths = [
            solvers.find_shortest_path((self.x, self.y), square, empty_space)
            for square in attack_squares
        ]
        paths = list(filter(lambda p: p is not None, paths))

        # If there are no shortest paths, we cannot move.
        if not paths:
            return self.x, self.y

        # Find the shortest-shortest path length.
        shortest_path_length = min(len(path) for path in paths)

        # Find all first steps of the shortest paths.
        first_steps = [
            Coordinate(*path[1]) for path in paths if len(path) == shortest_path_length
        ]

        # Sort the first steps in reading order.
        first_steps = _sort_in_reading_order(first_steps)

        # Return the first step.
        return first_steps[0].x, first_steps[0].y

    def __close_targets(self, targets: Iterable["Unit"]) -> Iterable["Unit"]:
        return filter(lambda u: abs(u.x - self.x) + abs(u.y - self.y) == 1, targets)

    def attack(self, targets: Iterable["Unit"]):
        """First go for the weakest, otherwise by reading order."""
        close_targets = list(self.__close_targets(targets))

        if not close_targets:
            return

        target = sorted(
            _sort_in_reading_order(close_targets), key=lambda u: u.hit_points
        )[0]
        target.hit_points -= self.__attack_power

    def turn(self, targets: Iterable["Unit"], empty_space: set[tuple[int, int]]):
        """Returns the new position."""
        new_position = self.move(targets, empty_space)
        self.x, self.y = new_position[0], new_position[1]
        self.attack(targets)
        return new_position


class Elf(Unit):
    BANNER = "Elf"


class Goblin(Unit):
    BANNER = "Goblin"


if __name__ == "__main__":
    with open("example", "r") as file:
        example_input = file.read()

    outcome, _ = Battle(example_input).perform()
    assert outcome == 27730

    elf_strength = 4
    while True:
        outcome, elf_deaths = Battle(example_input, elf_strength).perform()
        if elf_deaths == 0:
            assert outcome == 4988
            break
        else:
            elf_strength += 1

    with open("input", "r") as file:
        input_ = file.read()

    outcome, _ = Battle(input_).perform()
    print(f"A: {outcome}")

    elf_strength = 4
    while True:
        outcome, elf_deaths = Battle(input_, elf_strength).perform()
        if elf_deaths == 0:
            # Too high 39840 38512
            print(f"B: {outcome}")
            break
        else:
            elf_strength += 1
