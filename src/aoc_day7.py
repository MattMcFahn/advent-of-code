"""Solutions to day 7"""
from typing import List, Tuple, Dict


def setup_game(filepath: str) -> List[int]:
    """
    From the input filepath, reads the list of wait times for the game start, and sums to a dict
    with keys ranging from 0 to 8 inclusive
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [int(x) for x in lines[0].strip("\n").split(",")]
    return lines


def min_and_max(input_list: List) -> (int, int):
    """"""
    return min(input_list), max(input_list)


def lengths_from_point(input_list, point):
    """"""
    return [abs(x - point) for x in input_list]


def cost_from_distance(distance):
    """"""
    cost = sum(range(0, distance + 1))
    return cost


def cost_between_points(input_list, point):
    """"""
    distances = lengths_from_point(input_list, point)
    costs = [cost_from_distance(x) for x in distances]
    return costs


def total_cost(input_list):
    """"""
    return sum(input_list)


def challenge_one(input_list):
    """Wrap up steps for challenge one"""
    min, max = min_and_max(input_list)

    positions_and_cost = {
        x: total_cost(lengths_from_point(input_list, x)) for x in range(min, max + 1)
    }
    
    # TODO: Why is min giving a type error?
    cost = list((positions_and_cost.values()))
    cost.sort()
    cost = cost[0]
    position = [k for k, v in positions_and_cost.items() if v == cost][0]
    
    return position, cost


def challenge_two(input_list):
    """Wrap up challenge two"""
    min, max = min_and_max(input_list)

    positions_and_cost = {
        x: total_cost(cost_between_points(input_list, x)) for x in range(min, max + 1)
    }

    # TODO: Why is min giving a type error?
    cost = list((positions_and_cost.values()))
    cost.sort()
    cost = cost[0]
    position = [k for k, v in positions_and_cost.items() if v == cost][0]

    return position, cost


if __name__ == "__main__":
    FILEPATH = r'./resources/aoc-day7.txt'
    input_positions = setup_game(FILEPATH)

    # Challenge one
    position_one, cost_one = challenge_one(input_positions)
    print(f"Challenge one: {cost_one}")
    
    # Challenge two
    position_two, cost_two = challenge_two(input_positions)
    print(f"Challenge one: {cost_two}")

