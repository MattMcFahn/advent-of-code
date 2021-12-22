"""Solutions to day 17"""
from typing import Tuple, Dict, Union
from numpy import sign


def setup_game(filepath: str) -> Dict[str, Tuple[int, int]]:
    """
    From the input filepath, reads the input cube
    """
    with open(filepath) as file:
        lines = file.readlines()
    line = [x.strip("\n") for x in lines][0]

    y_coords = [int(number) for number in line[line.find(",") + 4 :].split("..")]
    x_coords = [int(number) for number in line[line.find("x") + 2 : line.find(",")].split("..")]
    input_range = {"x": (min(x_coords), max(x_coords)), "y": (min(y_coords), max(y_coords))}

    return input_range


def set_min_x_velocity(input_range: Dict[str, Tuple[int, int]]) -> (int, int):
    """Helper to get the min x velocity we need to consider - not tight"""
    position, min_x_velocity = 0, 0
    while position < input_range["x"][0]:
        min_x_velocity += 1
        position += min_x_velocity
    return min_x_velocity


def get_max_y_position(x_velocity: int, y_velocity: int, input_range: Dict) -> Union[None, int]:
    """For starting velocities and input range, return None if range not hit, or max y if it does"""
    current_step = 0
    x_coord, y_coord = (0, 0)
    max_y = 0
    while True:
        if current_step > 0:
            x_velocity -= sign(x_velocity)
            y_velocity -= 1
        x_coord += x_velocity
        y_coord += y_velocity
        max_y = y_coord if y_coord > max_y else max_y

        if (x_coord < -input_range["x"][0] or x_coord > input_range["x"][1]) or (
            y_coord < input_range["y"][0] or y_coord > -input_range["y"][1] * 100
        ):
            break
        if (
            input_range["x"][0] <= x_coord <= input_range["x"][1]
            and input_range["y"][0] <= y_coord <= input_range["y"][1]
        ):
            return max_y

        current_step += 1
    return None


def get_max_y_dict(input_range: Dict[str, Tuple[int, int]]) -> Dict[Tuple[int, int], int]:
    """Gets a dictionary of initial velocities that hit the target area, and the max y position attained for each"""
    min_x_velocity = set_min_x_velocity(input_range)
    max_hits = {}

    for x_velocity in range(min_x_velocity, input_range["x"][1] + 1):
        for y_velocity in range(-20000, 20000):
            max_y = get_max_y_position(x_velocity, y_velocity, input_range)
            if max_y is not None:
                max_hits[(x_velocity, y_velocity)] = max_y

    return max_hits


def challenge_one(y_dict: Dict[tuple, int]) -> int:
    """Completes challenge one"""
    return max(y_dict.values())


def challenge_two(y_dict: Dict[tuple, int]) -> int:
    """Completes challenge two"""
    return len(y_dict)


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day17.txt"
    target_range = setup_game(filepath=FILEPATH)
    max_y_dict = get_max_y_dict(input_range=target_range)

    # Challenge one
    challenge_one = challenge_one(y_dict=max_y_dict)
    print(f"Challenge one: {challenge_one}")

    # Challenge two
    challenge_two = challenge_two(y_dict=max_y_dict)
    print(f"Challenge two: {challenge_two}")
