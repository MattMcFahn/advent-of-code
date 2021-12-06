"""Solutions to day 6 of Advent of Code 2021"""
from typing import List, Dict, Tuple
from collections import Counter


def setup_game(filepath: str) -> List[int]:
    """
    From the input filepath, reads the list of wait times for the game start
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [int(x) for x in lines[0].strip("\n").split(",")]
    counted = Counter(lines)
    counted = {**{0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}, **counted}
    return counted


def increment_by_a_day(integer: int) -> int:
    """Moves one day down for values in (2, ..., 8). Moves 1 to 6"""
    if integer > 0:
        return integer - 1
    else:
        return 6


def get_next_days_population(population: List[int]) -> List[int]:
    """Gets population at the next day"""
    # new_population = [increment_by_a_day(x) for x in population] + [8]*population.count(0)
    return {
        **{x: population[x + 1] for x in population.keys() if x != 8},
        **{6: population[0] + population[7], 8: population[0]},
    }


def challenge_one(population, target_day):
    """
    Wraps up steps for chalenge one. Given starting population and times till birth, projects the population
    at day "target_day"
    """
    final_population = population.copy()
    for day in range(1, target_day + 1):
        final_population = get_next_days_population(final_population)

    return sum(final_population.values())


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
