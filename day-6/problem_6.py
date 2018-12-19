"""
Your first goal is to determine the order in which the steps should be completed. If more than one step is ready, choose the step which is first alphabetically. In this example, the steps would be completed as follows:

    Only C is available, and so it is done first.
    Next, both A and F are available. A is first alphabetically, so it is done next.
    Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically of the three.
    After that, only D and F are available. E is not available because only some of its prerequisites are complete. Therefore, D is completed next.
    F is the only choice, so it is done next.
    Finally, E is completed.

So, in this example, the correct order is CABDFE.

In what order should the steps in your instructions be completed?

--- Part Two ---

As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll go faster if we work together." Now, you need to account for multiple people working on steps simultaneously. If multiple steps are available, workers should still begin them in alphabetical order.

Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.

To simplify things for the example, however, suppose you only have help from one Elf (a total of two workers) and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26 seconds). Then, using the same instructions as above, this is how each second would be spent:

Second   Worker 1   Worker 2   Done
   0        C          .
   1        C          .
   2        C          .
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE

Each row represents one second of time. The Second column identifies how many seconds have passed as of the beginning of that second. Each worker column shows the step that worker is currently doing (or . if they are idle). The Done column shows completed steps.

Note that the order of the steps has changed; this is because steps now take time to finish and multiple workers can begin multiple steps simultaneously.

In this example, it would take 15 seconds for two workers to complete these steps.

With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?
"""

import copy
import re


JOB_CONSTANT_TIME = 60
WORKER_COUNT = 5

def job_time(name):
    return ord(name) - ord('A') + 1 + JOB_CONSTANT_TIME


class Worker:
    def __init__(self):
        self.busy = False
        self.working_on = ''
        self.seconds_remaining = None


if __name__ == '__main__':
    # Read input.
    with open('input', 'r') as file:
        dependencies = []
        for line in file:
            dependency = []

            # Find first.
            match = re.search('Step [A-Z]', line)
            if match:
                dependency.append(match.group(0).replace('Step ', ''))

            # Find second.
            match = re.search('step [A-Z]', line)
            if match:
                dependency.append(match.group(0).replace('step ', ''))

            # Add.
            dependencies.append(dependency)

    # Create the tracking structure:
    tracker = dict()
    for dependency in dependencies:
        if dependency[1] not in tracker.keys():
            tracker[dependency[1]] = set()
        if dependency[0] not in tracker.keys():
            tracker[dependency[0]] = set()
        tracker[dependency[1]].add(dependency[0])

    # Save a copy for part 2.
    tracker_copy = copy.copy(tracker)

    # Start the assembling loop.
    order = []
    while len(set(order)) != len(set(tracker.keys())):
        # Loop to find what is available.
        ready = []
        for key, value in tracker.items():
            if len(value) == 0 and key not in order:
                ready.append(key)

        # Sort ready.
        ready.sort()

        # Remove the ready[0] from all.
        set_ready = set([ready[0]])
        for key, value in tracker.items():
            tracker[key] = value - set_ready

        order.append(ready[0])

    answer_1 = ''.join(order)
    print(f'Answer 1 is {answer_1}.')

    # Now for the tricky part, we need a worker class.
    workers = []
    for _ in range(WORKER_COUNT):
        workers.append(Worker())

    # Each iteration is a second.
    seconds = 0
    done = []
    tracker = tracker_copy
    while len(set(done)) != len(set(tracker.keys())):
        # Free workers.
        for worker in workers:
            if worker.busy:
                worker.seconds_remaining -= 1
                if worker.seconds_remaining == 0:
                    for key, value in tracker.items():
                        tracker[key] = value - set([worker.working_on])
                    done.append(worker.working_on)
                    worker.busy = False
                    worker.working_one = ''

        # In progress.
        in_progress = [worker.working_on for worker in workers]

        # Loop to find what is available.
        ready = []
        for key, value in tracker.items():
            if len(value) == 0 and key not in done and key not in in_progress:
                ready.append(key)

        # Create queue.
        ready.sort()

        # Resolve workers.
        for worker in workers:
            if not worker.busy and len(ready) > 0:
                worker.working_on = ready.pop(0)
                print(job_time(worker.working_on))
                worker.seconds_remaining = job_time(worker.working_on)
                worker.busy = True

        # Report status.
        done.sort()
        status = [str(seconds)] + [worker.working_on for worker in workers] + [''.join(done)]
        print(' '.join(status))

        seconds += 1

    print(f'Answer 2 is {seconds-1}.')
