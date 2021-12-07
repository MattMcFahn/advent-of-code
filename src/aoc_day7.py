"""Solutions to day 7"""
from typing import List


def setup_game(filepath: str) -> List[int]:
    """
    From the input filepath, reads the list of wait times for the game start, and sums to a dict
    with keys ranging from 0 to 8 inclusive
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [int(x) for x in lines[0].strip("\n").split(",")]
    return lines


def lengths_from_point(input_list: List[int], point: int) -> List[int]:
    """Turn a list of positions and a target point into a list of distances from given point"""
    return [abs(x - point) for x in input_list]


def cost_from_distance(distance: int) -> int:
    """Sum from 1 to distance"""
    return sum(range(0, distance + 1))


def cost_between_points(input_list: List[int], point: int) -> List[int]:
    """
    For an input_list of positions, and a target point, return a list of arithmetic sums from each position to the point
    """
    distances = lengths_from_point(input_list, point)
    costs = [cost_from_distance(x) for x in distances]
    return costs


def challenge_answers(input_list: List[int], challenge: int) -> (int, int):
    """Wrap up steps for challenge one and two"""
    minimum, maximum = min(input_list), max(input_list)

    functions = {1: lengths_from_point, 2: cost_between_points}

    positions_and_cost = {x: sum(functions[challenge](input_list, x)) for x in range(minimum, maximum + 1)}

    # TODO: Why is min giving a type error?
    cost = list((positions_and_cost.values()))
    cost.sort()
    cost = cost[0]
    position = [k for k, v in positions_and_cost.items() if v == cost][0]

    return position, cost


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day7.txt"
    input_positions = setup_game(FILEPATH)

    # Challenge one
    _, cost_one = challenge_answers(input_list=input_positions, challenge=1)
    print(f"Challenge one: {cost_one}")

    # Challenge two
    _, cost_two = challenge_answers(input_list=input_positions, challenge=2)
    print(f"Challenge one: {cost_two}")
