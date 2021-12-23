"""Solutions to day 17"""
from typing import Tuple, Dict, List
from itertools import product


def instruction_is_in_bootup(instruction: Dict[str, int]) -> bool:
    """Tests whether the instruction intersects with cube (-50, -50, -50) to (50, 50, 50)"""
    miss = (
        (instruction["x"][0] > 50 or instruction["x"][1] < -50)
        or (instruction["y"][0] > 50 or instruction["y"][1] < -50)
        or (instruction["z"][0] > 50 or instruction["z"][1] < -50)
    )
    return not miss


def setup_game(filepath: str) -> (Dict[Tuple[int, int, int], int], List[Dict[str, int]]):
    """
    From the input filepath, reads the input cube
    """
    start_instructions = []
    with open(filepath) as file:
        for line in file:
            line = line.strip("\n")
            x_line = line[line.find("x") + 2 :]
            x_line = x_line[: x_line.find(",")]
            y_line = line[line.find("y") + 2 :]
            y_line = y_line[: y_line.find("z") - 1]
            z_line = line[line.find("z") + 2 :]
            instruction = {
                "instruction": line[: line.find(" ")],
                "x": (min([int(num) for num in x_line.split("..")]), max([int(num) for num in x_line.split("..")])),
                "y": (min([int(num) for num in y_line.split("..")]), max([int(num) for num in y_line.split("..")])),
                "z": (min([int(num) for num in z_line.split("..")]), max([int(num) for num in z_line.split("..")])),
            }

            instruction["range"] = product(
                range(instruction["x"][0], instruction["x"][1] + 1),
                range(instruction["y"][0], instruction["y"][1] + 1),
                range(instruction["z"][0], instruction["z"][1] + 1),
            )

            start_instructions.append(instruction)

    cube_range = range(-50, 51)
    start_cube = {(x, y, z): 0 for (x, y, z) in product(cube_range, cube_range, cube_range)}

    return start_cube, start_instructions


def get_target_points(instruction: Dict[str, int]):
    """TODO"""
    x_range = range(instruction["x"][0], instruction["x"][1] + 1)
    y_range = range(instruction["y"][0], instruction["y"][1] + 1)
    z_range = range(instruction["z"][0], instruction["z"][1] + 1)

    return product(x_range, y_range, z_range)


def change_points(cube, target_points, instruction_type: str):
    """TODO"""
    number = {"on": 1, "off": 0}[instruction_type]

    for point in target_points:
        cube[point] = number
    return cube


def challenge_one(cube: Dict[Tuple[int, int, int], int], instructions: List[Dict[str, int]]) -> int:
    """Completes challenge one"""
    for instruction in instructions:
        if instruction_is_in_bootup(instruction):
            target_points = get_target_points(instruction)
            cube = change_points(cube, target_points, instruction["instruction"])

    return sum(cube.values())


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day22.txt"
    print("Setup game... ")
    activity_cube, input_instructions = setup_game(filepath=FILEPATH)
    print("Setup game... DONE")

    # Challenge one
    print("Running challenge one...")
    challenge_one = challenge_one(cube=activity_cube, instructions=input_instructions)
    print(f"Challenge one: {challenge_one}")

    # # Challenge two
    # TODO: Work with intersections of ranges
    # challenge_two = challenge_two(instructions=input_instructions)
    # print(f"Challenge one: {challenge_two}")
