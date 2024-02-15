import re
import collections

from src.day_protocol import AocDay
from src.device.device import Device


class Day19(AocDay):
    def part_a(self, input_: str) -> str:
        device = Device(input_)
        register = device.run([0] * 6)
        return str(register[0])

    def part_b(self, input_: str) -> str:
        """I don't find this reverse engineering fun, so I looked at some solutions and try to get the gist.

        Credit to /u/asger_blahimmel.
        """
        input_lines = input_.split("\n")
        a, b = map(int, [re.findall(r"\d+", input_lines[i])[1] for i in [22, 24]])
        number_to_factorize = 10551236 + a * 22 + b

        factors = collections.defaultdict(lambda: 0)
        possible_prime_divisor = 2

        while possible_prime_divisor ** 2 <= number_to_factorize:
            while number_to_factorize % possible_prime_divisor == 0:
                number_to_factorize /= possible_prime_divisor
                factors[possible_prime_divisor] += 1
            possible_prime_divisor += 1

        if number_to_factorize > 1:
            factors[number_to_factorize] += 1

        sum_of_divisors = 1
        for prime_factor in factors:
            sum_of_divisors *= (prime_factor ** (factors[prime_factor] + 1) - 1) / (
                    prime_factor - 1
            )

        return str(int(sum_of_divisors))
