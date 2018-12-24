"""
The immune system and the infection each have an army made up of several groups; each group consists of one or more identical units. The armies repeatedly fight until only one army has units remaining.

Units within a group all have the same hit points (amount of damage a unit can take before it is destroyed), attack damage (the amount of damage each unit deals), an attack type, an initiative (higher initiative units attack first and win ties), and sometimes weaknesses or immunities. Here is an example group:

18 units each with 729 hit points (weak to fire; immune to cold, slashing)
 with an attack that does 8 radiation damage at initiative 10

Each group also has an effective power: the number of units in that group multiplied by their attack damage. The above group has an effective power of 18 * 8 = 144. Groups never have zero or negative units; instead, the group is removed from combat.

Each fight consists of two phases: target selection and attacking.

During the target selection phase, each group attempts to choose one target. In decreasing order of effective power, groups choose their targets; in a tie, the group with the higher initiative chooses first. The attacking group chooses to target the group in the enemy army to which it would deal the most damage (after accounting for weaknesses and immunities, but not accounting for whether the defending group has enough units to actually receive all of that damage).

If an attacking group is considering two defending groups to which it would deal equal damage, it chooses to target the defending group with the largest effective power; if there is still a tie, it chooses the defending group with the highest initiative. If it cannot deal any defending groups damage, it does not choose a target. Defending groups can only be chosen as a target by one attacking group.

At the end of the target selection phase, each group has selected zero or one groups to attack, and each group is being attacked by zero or one groups.

During the attacking phase, each group deals damage to the target it selected, if any. Groups attack in decreasing order of initiative, regardless of whether they are part of the infection or the immune system. (If a group contains no units, it cannot attack.)

The damage an attacking group deals to a defending group depends on the attacking group's attack type and the defending group's immunities and weaknesses. By default, an attacking group would deal damage equal to its effective power to the defending group. However, if the defending group is immune to the attacking group's attack type, the defending group instead takes no damage; if the defending group is weak to the attacking group's attack type, the defending group instead takes double damage.

The defending group only loses whole units from damage; damage is always dealt in such a way that it kills the most units possible, and any remaining damage to a unit that does not immediately kill it is ignored. For example, if a defending group contains 10 units with 10 hit points each and receives 75 damage, it loses exactly 7 units and is left with 3 units at full health.

After the fight is over, if both armies still contain units, a new fight begins; combat only ends once one army has lost all of its units.

You scan the reindeer's condition (your puzzle input); the white-bearded man looks nervous. As it stands now, how many units would the winning army have?

--- Part Two ---

Things aren't looking good for the reindeer. The man asks whether more milk and cookies would help you think.

If only you could give the reindeer's immune system a boost, you might be able to change the outcome of the combat.

A boost is an integer increase in immune system units' attack damage.

How many units does the immune system have left after getting the smallest boost it needs to win?
"""

from copy import deepcopy
import re


DEBUG = False


class Group:
    def __init__(self, count, hp, initiative, dmg, dmg_type, weak: list, immune: list):
        self.count = count
        self.hp = hp
        self.initiative = initiative
        self.dmg = dmg
        self.dmg_type = dmg_type
        self.weak = weak
        self.immune = immune

    def calculate_damage(self, attacker):
        dmg = attacker.effective_power

        if attacker.dmg_type in self.weak:
            dmg *= 2
        elif attacker.dmg_type in self.immune:
            dmg *= 0

        return dmg

    def defend(self, army, key, own_key):
        dmg = self.calculate_damage(army.groups[key])
        kill_count = min(self.count, dmg // self.hp)
        self.count -= kill_count

        if DEBUG:
            print(f'{army.name} group {key} attacks defending group {own_key}, killing {kill_count} units.')

    @property
    def effective_power(self):
        return self.count * self.dmg


class Army:
    def __init__(self, name):
        self.name = name
        self.groups = dict()

    @property
    def alive(self):
        if sum([g.count for g in self.groups.values()]) > 0:
            return True
        else:
            return False

    @property
    def alive_count(self):
        return sum([g.count for g in self.groups.values()])

    def add_group(self, group):
        index = len(self.groups) + 1
        self.groups[index] = group

    def find_target(self, attacker_group_key, target_armies, exclude_defend):
        target_army = None
        target_key = None
        target_damage = 0
        target_ep = 0
        target_init = 0

        for army in target_armies.values():
            if army.name == self.name:
                continue

            for k, v in army.groups.items():
                if v in exclude_defend:
                    continue

                dmg = v.calculate_damage(self.groups[attacker_group_key])

                if dmg == 0:
                    continue

                if DEBUG:
                    print(f'{self.name} group {attacker_group_key} would deal defending group {k} {dmg} damage.')

                if (dmg > target_damage) or (dmg == target_damage and v.effective_power > target_ep) or \
                    (dmg == target_damage and v.effective_power == target_ep and v.initiative > target_init):
                    target_army = army
                    target_damage = dmg
                    target_key = k
                    target_ep = v.effective_power
                    target_init = v.initiative

        return target_damage, target_army, target_key


def battle(armies, boost=0):
    # Apply the boost.
    for group in armies['Immune System'].groups.values():
        group.dmg += boost

    last_remaining_count = 0
    while False not in [x.alive for x in armies.values()]:
        # Find targets.
        targets = []

        for army in list(armies.values())[::-1]:
            # Get all groups : army combinations.
            exclude_defend = []
            combinations = []
            for gk in army.groups.keys():
                combinations.append([army, gk])

            combinations.sort(key=lambda row: (-row[0].groups[row[1]].effective_power, -row[0].groups[row[
                1]].initiative))

            for combination in combinations:
                damage, target_army, target_group_key = combination[0].find_target(combination[1], armies,
                                                                                   exclude_defend)
                if target_army is None:
                    continue

                target = dict()
                target['target_army'] = target_army
                target['target_group_key'] = target_group_key
                target['attack_army'] = combination[0]
                target['attack_group_key'] = combination[1]

                targets.append(target)
                exclude_defend.append(target_army.groups[target_group_key])

        targets.sort(key=lambda d: -d['attack_army'].groups[d['attack_group_key']].initiative)

        for target in targets:
            try:
                target['target_army'].groups[target['target_group_key']].defend(target['attack_army'],
                                                                                target['attack_group_key'],
                                                                                target['target_group_key'])
            except KeyError:
                if DEBUG:
                    print(f'Deleted group {target["attack_group_key"]} from '
                          f'{target["attack_army"].name} cannot do anything.')

            if target['target_army'].groups[target['target_group_key']].count == 0:
                del target['target_army'].groups[target['target_group_key']]

                if DEBUG:
                    print(f'Deleted group {target["attack_group_key"]} from {target["attack_army"].name}.')

        if DEBUG:
            print(f'Battle status: {armies["Immune System"].alive_count} and {armies["Infection"].alive_count}.')

        remaining_count = sum([a.alive_count for a in armies.values()])

        if remaining_count == last_remaining_count:
            return None, None
        else:
            last_remaining_count = remaining_count

    if armies['Immune System'].alive_count > 0:
        return True, remaining_count
    else:
        return False, remaining_count


if __name__ == '__main__':
    # Read input.
    with open('input', 'r') as file:
        current_army = None
        armies = dict()
        group_count = 0

        for line in file:
            match = re.match('([A-z\s]+):', line)
            if match:
                current_army = match.group(1)
                armies[current_army] = Army(current_army)

            match = re.match('([0-9]+) units each with ([0-9]+) hit points \(([^\)]+)\) with an attack that does (['
                             '0-9]+) ([a-z]+) damage at initiative ([0-9]+)', line)
            if match:
                group_count += 1
                count = int(match.group(1))
                hp = int(match.group(2))
                dmg = int(match.group(4))
                dmg_type = match.group(5)
                initiative = int(match.group(6))
                weak = []
                immune = []

                match_weak = re.search('weak to ([a-z,\s]+)', match.group(3))
                if match_weak:
                    weak = match_weak.group(1).split(', ')

                match_immune = re.search('immune to ([a-z,\s]+)', match.group(3))
                if match_immune:
                    immune = match_immune.group(1).split(', ')

                armies[current_army].add_group(Group(count, hp, initiative, dmg, dmg_type, weak, immune))

            match = re.match('([0-9]+) units each with ([0-9]+) hit points with an attack that does (['
                             '0-9]+) ([a-z]+) damage at initiative ([0-9]+)', line)
            if match:
                group_count += 1
                count = int(match.group(1))
                hp = int(match.group(2))
                dmg = int(match.group(3))
                dmg_type = match.group(4)
                initiative = int(match.group(5))
                weak = []
                immune = []

                armies[current_army].add_group(Group(count, hp, initiative, dmg, dmg_type, weak, immune))

    _, remaining_count = battle(deepcopy(armies))
    print(f'Answer 1 is {remaining_count}.')

    # Now loop over increasing integers and see if this does not take too long.
    boost = 0

    last_won = False
    last_remaining_count = 0
    while not last_won:
        boost += 1
        last_won, last_remaining_count = battle(deepcopy(armies), boost)
        if last_won is None:
            print('They tied!')
        elif not last_won:
            print(f'The immune system lost with {last_remaining_count}')

    print(f'Answer 2 is {last_remaining_count}.')

