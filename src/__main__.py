"""Runs all days."""
from src.day_protocol import AocDay


def dynamic_object_import(module_name, object_name):
    try:
        module = __import__(module_name, fromlist=[object_name])
        obj = getattr(module, object_name)
        return obj
    except ImportError:
        print(f"Object '{object_name}' not found in module '{module_name}'.")
        return None


def get_input(day_number_: int) -> str:
    with open(f"../inputs/{day_number_}.txt", "r") as file:
        return file.read().rstrip()


if __name__ == "__main__":
    for day_number in range(16, 26):
        try:
            day: AocDay = dynamic_object_import(
                f"days.problem_{day_number}", f"Day{day_number}"
            )()
        except TypeError:
            continue
        input_ = get_input(day_number)
        print(f"Day {day_number}a: {day.part_a(input_)}")
        print(f"Day {day_number}b: {day.part_b(input_)}")
