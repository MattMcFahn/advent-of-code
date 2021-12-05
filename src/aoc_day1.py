"""Solutions for day 1"""
from typing import List


def get_input(filepath: str) -> List[int]:
    """Simple helper to get useful data structures from input"""
    with open(filepath) as file:
        lines = file.readlines()

    return lines


def make_sliding_window(input_values: List) -> List:
    """Helper that takes a list of length n and returns a list of length (n-3),
     where element i = sum ( elem_i, elem_(i-1), elem_(i-2) )
    """
    summed_values = [
        input_values[i] + input_values[i - 1] + input_values[i - 2]
        for i in range(2, len(input_values))
    ]
    return summed_values


def get_increase_count(input_values: List) -> int:
    """Counts the number of increases between corresponding entries in the list of input_values"""
    counter = 0

    previous = input_values.pop(0)
    while input_values:
        current = input_values.pop(0)
        if current > previous:
            counter += 1
        previous = current

    return counter


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day1.txt"
    values = get_input(FILEPATH)

    # Part 1, increase count on values
    challenge_one = get_increase_count(values)
    print(f"Challenge one: {challenge_one}")

    # Part 2, increase count on window values
    window_values = make_sliding_window(values)
    window_result = get_increase_count(window_values)
    print(f"Challenge two: {window_result}")
