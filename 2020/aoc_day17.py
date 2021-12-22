"""Solutions to day 17"""
from typing import Tuple, Dict
from itertools import product


def setup_game(filepath: str, num_steps: int) -> Dict[Tuple[int, int, int], int]:
    """
    From the input filepath, reads the input cube
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [list(x.strip("\n").replace(".", "0").replace("#", "1")) for x in lines]

    if num_steps:
        lines = [["0"] * num_steps * 2 + x + ["0"] * num_steps * 2 for x in lines]
        lines = [["0"] * len(lines[0])] * num_steps * 2 + lines + [["0"] * len(lines[0])] * num_steps * 2

    midpoint = int((len(lines) - 1) / 2)

    empty_z_range = [x for x in range(0, len(lines)) if x != midpoint]
    cube_range = range(0, len(lines))

    activity_dict = {
        **{(x, y, midpoint): int(lines[x][y]) for x, y in product(cube_range, cube_range)},
        **{(x, y, z): 0 for (x, y, z) in product(cube_range, cube_range, empty_z_range)},
    }

    return activity_dict


def get_active_neighbours(cube: Dict[Tuple[int, int, int], int], point: Tuple[int, int, int]) -> int:
    """Finds the number of active neighbours from a point in the cube"""
    x_coord = point[0]
    y_coord = point[1]
    z_coord = point[2]

    x_range = range(x_coord - 1, x_coord + 2)
    y_range = range(y_coord - 1, y_coord + 2)
    z_range = range(z_coord - 1, z_coord + 2)

    min_coord = 0
    max_coord = max(cube.keys())[0]

    neighbouring_points = [
        (x, y, z)
        for (x, y, z) in product(x_range, y_range, z_range)
        if (x, y, z) != (x_coord, y_coord, z_coord)
        and not (
            (x > max_coord or x < min_coord) or (y > max_coord or y < min_coord) or (z > max_coord or z < min_coord)
        )
    ]

    return sum(cube[neighbour] for neighbour in neighbouring_points)


def simulate_step(cube: Dict[Tuple[int, int, int], int]) -> Dict[Tuple[int, int, int], int]:
    """Simulates a single step in the changing of the cube"""
    new_cube = cube.copy()
    for point in cube.keys():
        active_neighbours = get_active_neighbours(cube=cube, point=point)
        if cube[point]:  # == 1
            if active_neighbours in {2, 3}:
                new_cube[point] = 1
            else:
                new_cube[point] = 0
        else:  # cube[point] == 0
            if active_neighbours == 3:
                new_cube[point] = 1
            else:
                new_cube[point] = 0
    return new_cube


def challenge_one(cube: Dict[Tuple[int, int, int], int]) -> int:
    """Solves challenge one"""
    target_steps = 6
    for _ in range(0, target_steps):
        print(f"Step: {_ + 1}")
        cube = simulate_step(cube)

    return sum(cube.values())


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day17.txt"
    activity_cube = setup_game(filepath=FILEPATH, num_steps=6)

    # Challenge one
    challenge_one = challenge_one(cube=activity_cube)
    print(f"Challenge one: {challenge_one}")

    # # Challenge two
    # challenge_two = challenge_two(packet_object=packet)
    # print(f"Challenge one: {challenge_two}")
    #
