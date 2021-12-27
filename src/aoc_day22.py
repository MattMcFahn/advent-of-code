"""Solutions to day 22"""
from typing import Dict, List
from itertools import product


def instruction_is_in_bootup(instruction: Dict[str, int]) -> bool:
    """Tests whether the instruction intersects with cube (-50, -50, -50) to (50, 50, 50). Used for challenge one"""
    miss = (
        (instruction["x"][0] > 50 or instruction["x"][1] < -50)
        or (instruction["y"][0] > 50 or instruction["y"][1] < -50)
        or (instruction["z"][0] > 50 or instruction["z"][1] < -50)
    )
    return not miss


def setup_game(filepath: str) -> (Dict[str, int], List[Dict[str, int]]):
    """
    From the input filepath, reads the input instructions (and a helper cube for challenge one)
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

            start_instructions.append(instruction)

    cube_range = range(-50, 51)
    start_cube = {(x, y, z): 0 for (x, y, z) in product(cube_range, cube_range, cube_range)}

    return start_cube, start_instructions


def get_target_points(instruction: Dict[str, int]) -> product:
    """Implemented in easy method for challenge one - get a range of points in a cube as a cartesian outer product"""
    x_range = range(instruction["x"][0], instruction["x"][1] + 1)
    y_range = range(instruction["y"][0], instruction["y"][1] + 1)
    z_range = range(instruction["z"][0], instruction["z"][1] + 1)

    return product(x_range, y_range, z_range)


def change_points(cube: Dict[str, int], target_points: product, instruction_type: str) -> Dict[str, int]:
    """Implemented in the easy method for challenge one - switch cubes on/off"""
    number = {"on": 1, "off": 0}[instruction_type]

    for point in target_points:
        cube[point] = number
    return cube


def challenge_one(cube: Dict[str, int], instructions: List[Dict[str, int]]) -> int:
    """Completes challenge one"""
    for instruction in instructions:
        if instruction_is_in_bootup(instruction):
            target_points = get_target_points(instruction)
            cube = change_points(cube, target_points, instruction["instruction"])

    return sum(cube.values())


def intersects(instruction_one: Dict[str, int], instruction_two: Dict[str, int]) -> bool:
    """Helper to identify whether two cubes intersect"""
    if not (instruction_one["x"][0] <= instruction_two["x"][1] and instruction_one["x"][1] >= instruction_two["x"][0]):
        return False

    if not (instruction_one["y"][0] <= instruction_two["y"][1] and instruction_one["y"][1] >= instruction_two["y"][0]):
        return False

    if not (instruction_one["z"][0] <= instruction_two["z"][1] and instruction_one["z"][1] >= instruction_two["z"][0]):
        return False

    return True


def get_intersection(instruction_one: Dict[str, int], instruction_two: Dict[str, int]) -> Dict[str, int]:
    """Helper to get a sub cuboid as the intersection of two cuboids"""
    if instruction_one["instruction"] == instruction_two["instruction"]:
        change = {"on": "off", "off": "on"}[instruction_one["instruction"]]
    else:
        change = instruction_one["instruction"]

    min_x = max(instruction_one["x"][0], instruction_two["x"][0])
    max_x = min(instruction_one["x"][1], instruction_two["x"][1])
    min_y = max(instruction_one["y"][0], instruction_two["y"][0])
    max_y = min(instruction_one["y"][1], instruction_two["y"][1])
    min_z = max(instruction_one["z"][0], instruction_two["z"][0])
    max_z = min(instruction_one["z"][1], instruction_two["z"][1])

    new_instruction = {"instruction": change, "x": (min_x, max_x), "y": (min_y, max_y), "z": (min_z, max_z)}
    return new_instruction


def volume(instruction: Dict[str, int]) -> int:
    """Helper to get volume of a cube"""
    return (
        (instruction["x"][1] - instruction["x"][0] + 1)
        * (instruction["y"][1] - instruction["y"][0] + 1)
        * (instruction["z"][1] - instruction["z"][0] + 1)
    )


def get_intersecting_cuboids(instructions: List[Dict[str, int]]) -> List[Dict[str, int]]:
    """Applies the main logic described in `challenge_two`"""
    intersecting_cuboids = []

    for _, instruction in enumerate(instructions):
        print(f"Instruction: {_}")
        intersections = []
        for cuboid in intersecting_cuboids:
            if intersects(instruction, cuboid):
                intersection = get_intersection(instruction, cuboid)
                intersections.append(intersection)

        for intersection in intersections:
            intersecting_cuboids.append(intersection)

        if instruction["instruction"] == "on":
            intersecting_cuboids.append(instruction)
        print(f"Size of distinct cuboids: {len(intersecting_cuboids)}")
    return intersecting_cuboids


def challenge_two(instructions: List[Dict[str, int]]) -> int:
    """Completes challenge two. The strategy is that:
        * As we consider a new input cuboid, we compare against a list of cuboids we know we can end up just summing
        volumes for to get the answer (`intersecting_cuboids`).
        * In considering a new (`instruction`), we test if it intersects with each `cuboid` in `intersecting_cuboids`.
            * If it intersects, we get a new sub-cuboid of the intersection.
                - If both the originals are to be turned 'on', we turn 'off' the intersection. Vice-versa for 'off'
                - Else we turn the intersection to match the first cuboid
            * We append all intersections before appending the input cuboid to `intersecting_cuboids`
        * We sum volumes over all the intersecting cuboids
    """
    intersecting_cuboids = get_intersecting_cuboids(instructions)
    value = sum([volume(cuboid) * {"on": 1, "off": -1}[cuboid["instruction"]] for cuboid in intersecting_cuboids])

    return value


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
    challenge_two = challenge_two(instructions=input_instructions)
    print(f"Challenge two: {challenge_two}")
