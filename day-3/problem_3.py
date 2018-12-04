"""
The columns are Date, which shows the month-day portion of the relevant day; ID, which shows the guard on duty that day; and Minute, which shows the minutes during which the guard was asleep within the midnight hour. (The Minute column's header shows the minute's ten's digit in the first row and the one's digit in the second row.) Awake is shown as ., and asleep is shown as #.

Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they wake up. For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard into working tonight so you can have the best chance of sneaking in. You have two strategies for choosing the best guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order, your entries are in the order you found them. You'll need to organize them before they can be analyzed.

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 10 * 24 = 240.)
"""

from datetime import datetime, timedelta
import re


if __name__ == '__main__':
    # Get the raw input.
    raw_input = []
    with open('input', 'r') as file:
        for line in file:
            raw_input.append(line)
    raw_input.sort()

    # Our empty data structure.
    sleeping_schedule = dict()

    # Variable required for looping.
    current_guard = None
    falling_asleep_ts = None

    for line in raw_input:
        raw_ts = re.search('(1518-[0-1][0-9]-[0-3][0-9] [0-9][0-9]:[0-9][0-9])', line).group(0)
        ts = datetime.strptime(raw_ts, '%Y-%m-%d %H:%M')

        # Check for change of guard.
        match = re.search('#[0-9]+', line)
        if match:
            current_guard = int(match.group(0).replace('#', ''))
            if current_guard not in list(sleeping_schedule.keys()):
                sleeping_schedule[current_guard] = dict()

        # Check for falling asleep.
        match = re.search('asleep', line)
        if match:
            falling_asleep_ts = ts

        # Check for waking up.
        match = re.search('wakes up', line)
        if match:
            # Add minutes to the falling asleep timestamp until it match the current.
            while ts != falling_asleep_ts: # TODO: which minute does he wake?
                falling_asleep_ts = falling_asleep_ts + timedelta(minutes=1)
                minute = int(falling_asleep_ts.strftime('%M'))
                if minute not in list(sleeping_schedule[current_guard].keys()):
                    sleeping_schedule[current_guard][minute] = 1
                else:
                    sleeping_schedule[current_guard][minute] += 1

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

    print('Answer 1 is {}*{}={}.'.format(sleepiest_guard[0], sleepiest_minute[0], sleepiest_guard[0] * sleepiest_minute[0]))
