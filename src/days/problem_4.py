import re
from datetime import datetime, timedelta

from src.day_protocol import AocDay


class Day4(AocDay):
    def part_a(self, input_: str) -> str:
        # Get the raw input.
        raw_input = []
        for line in input_.split("\n"):
            if line:
                raw_input.append(line)
        raw_input.sort()

        # Our empty data structure.
        sleeping_schedule = dict()

        # Variable required for looping.
        current_guard = None
        falling_asleep_ts = None

        for line in raw_input:
            raw_ts = re.search(
                "(1518-[0-1][0-9]-[0-3][0-9] [0-9][0-9]:[0-9][0-9])", line
            ).group(0)
            ts = datetime.strptime(raw_ts, "%Y-%m-%d %H:%M")

            # Check for change of guard.
            match = re.search("#[0-9]+", line)
            if match:
                current_guard = int(match.group(0).replace("#", ""))
                if current_guard not in list(sleeping_schedule.keys()):
                    sleeping_schedule[current_guard] = dict()

            # Check for falling asleep.
            match = re.search("asleep", line)
            if match:
                falling_asleep_ts = ts

            # Check for waking up.
            match = re.search("wakes up", line)
            if match:
                # Add minutes to the falling asleep timestamp until it match the current.
                while ts != falling_asleep_ts:
                    minute = int(falling_asleep_ts.strftime("%M"))
                    if minute not in list(sleeping_schedule[current_guard].keys()):
                        sleeping_schedule[current_guard][minute] = 1
                    else:
                        sleeping_schedule[current_guard][minute] += 1
                    falling_asleep_ts = falling_asleep_ts + timedelta(minutes=1)

        # Calculate the most sleepy guard.
        def sleepsum(x):
            result = 0
            for key in x.keys():
                result += x[key]
            return result

        sleepiest_guard = [-1, -1]
        for key in sleeping_schedule.keys():
            if sleepsum(sleeping_schedule[key]) > sleepiest_guard[1]:
                sleepiest_guard[0] = key
                sleepiest_guard[1] = sleepsum(sleeping_schedule[key])

        # Find the most slept minute.
        sleepiest_minute = [-1, -1]
        for key in sleeping_schedule[sleepiest_guard[0]].keys():
            if sleeping_schedule[sleepiest_guard[0]][key] > sleepiest_minute[1]:
                sleepiest_minute[0] = key
                sleepiest_minute[1] = sleeping_schedule[sleepiest_guard[0]][key]

        return str(sleepiest_guard[0] * sleepiest_minute[0])

    def part_b(self, input_: str) -> str:
        # Get the raw input.
        raw_input = []
        for line in input_.split("\n"):
            if line:
                raw_input.append(line)
        raw_input.sort()

        # Our empty data structure.
        sleeping_schedule = dict()

        # Variable required for looping.
        current_guard = None
        falling_asleep_ts = None

        for line in raw_input:
            raw_ts = re.search(
                "(1518-[0-1][0-9]-[0-3][0-9] [0-9][0-9]:[0-9][0-9])", line
            ).group(0)
            ts = datetime.strptime(raw_ts, "%Y-%m-%d %H:%M")

            # Check for change of guard.
            match = re.search("#[0-9]+", line)
            if match:
                current_guard = int(match.group(0).replace("#", ""))
                if current_guard not in list(sleeping_schedule.keys()):
                    sleeping_schedule[current_guard] = dict()

            # Check for falling asleep.
            match = re.search("asleep", line)
            if match:
                falling_asleep_ts = ts

            # Check for waking up.
            match = re.search("wakes up", line)
            if match:
                # Add minutes to the falling asleep timestamp until it match the current.
                while ts != falling_asleep_ts:
                    minute = int(falling_asleep_ts.strftime("%M"))
                    if minute not in list(sleeping_schedule[current_guard].keys()):
                        sleeping_schedule[current_guard][minute] = 1
                    else:
                        sleeping_schedule[current_guard][minute] += 1
                    falling_asleep_ts = falling_asleep_ts + timedelta(minutes=1)

        # Calculate the most sleepy guard.
        def sleepsum(x):
            result = 0
            for key in x.keys():
                result += x[key]
            return result

        sleepiest_guard = [-1, -1]
        for key in sleeping_schedule.keys():
            if sleepsum(sleeping_schedule[key]) > sleepiest_guard[1]:
                sleepiest_guard[0] = key
                sleepiest_guard[1] = sleepsum(sleeping_schedule[key])

        # Find the most consistently sleepy guard.
        sleepiest_consistent = [-1, -1, -1]
        for guard in sleeping_schedule.keys():
            for minute in sleeping_schedule[guard].keys():
                if sleeping_schedule[guard][minute] > sleepiest_consistent[2]:
                    sleepiest_consistent[0] = guard
                    sleepiest_consistent[1] = minute
                    sleepiest_consistent[2] = sleeping_schedule[guard][minute]

        return str(sleepiest_consistent[0] * sleepiest_consistent[1])
