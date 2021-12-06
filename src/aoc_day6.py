"""Solutions for day 6"""
from typing import Dict
from collections import Counter


def setup_game(filepath: str) -> Dict[int, int]:
    """
    From the input filepath, reads the list of wait times for the game start, and sums to a dict
    with keys ranging from 0 to 8 inclusive
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [int(x) for x in lines[0].strip("\n").split(",")]
    counted = Counter(lines)
    counted = {**{0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}, **counted}
    return counted


def increment_by_a_day(integer: int) -> int:
    """Moves one day down for values in (2, ..., 8). Moves 1 to 6"""
    return integer - 1 if integer > 0 else 6


def get_next_days_population(population: Dict[int, int]) -> Dict[int, int]:
    """Gets population at the next day"""
    return {
        **{x: population[x + 1] for x in population.keys() if x != 8},
        **{6: population[0] + population[7], 8: population[0]},
    }


def challenge_one(population: Dict[int, int], target_day: int) -> int:
    """
    Wraps up steps for chalenge one. Given starting population and times till birth, projects the
    population at day "target_day"
    """
    dynamic_population = population.copy()
    for _ in range(1, target_day + 1):
        dynamic_population = get_next_days_population(dynamic_population)

    return sum(dynamic_population.values())


if __name__ == "__main__":
    FILEPATH = "./resources/aoc-day6.txt"
    input_times = setup_game(FILEPATH)
    input_day = 80

    # Challenge one
    final_population = challenge_one(population=input_times, target_day=input_day)
    print(f"Challenge one: {final_population}")

    # Challenge two
    second_day = 256
    second_population = challenge_one(population=input_times, target_day=second_day)
    print(f"Challenge two: {second_population}")
