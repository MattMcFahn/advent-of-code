"""Solutions for day 2"""

from typing import Tuple, List, Dict


def get_input(filepath: str) -> Tuple[List, Dict]:
    """Simple helper to get useful data structures from input"""
    with open(filepath) as file:
        lines = file.readlines()
    keyed = {line[: len(line) - 2] for line in lines}
    return lines, keyed


def calculate_answer(input_values: List) -> Tuple[int, int, int]:
    """Calculations for challenge two"""
    values_mapped = [(x[: len(x) - 2], int(x[-1])) for x in input_values]

    aim = 0
    horizontal = 0
    depth = 0
    for value in values_mapped:
        target = value[0]
        increment = value[1]

        if target == "forward":
            horizontal += increment
            depth += increment * aim
        if target == "up":
            aim -= increment
        if target == "down":
            aim += increment

    return aim, depth, horizontal


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day2.txt"
    values, keys = get_input(FILEPATH)
    summed_values = {key: sum([int(x[-1]) for x in values if key in x]) for key in keys}

    challenge_one = (summed_values["down"] - summed_values["up"]) * summed_values["forward"]
    print(f"Challenge one: {challenge_one}")

    final_aim, final_depth, final_horizontal = calculate_answer(values)

    challenge_two = final_depth * final_horizontal
    print(f"Challenge two: {challenge_two}")
