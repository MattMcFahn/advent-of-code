"""Solutions to day 8"""
from math import prod
from typing import List, Tuple


def setup_game(filepath: str) -> List[str]:
    """
    From the input filepath, read and sort the input strings
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [list(x.strip("\n")) for x in lines]
    # frame = pd.DataFrame(lines)

    return lines


def get_low_points(lines: List[List[str]]) -> List[Tuple[int, int, int]]:
    """Helper to get low points with double enumerate.

    Return values in the list are:
        * Value at low point
        * Row index
        * Column index
    """
    low_points = []
    for row_index, line in enumerate(lines):
        for col_index, entry in enumerate(line):
            surrounding_entries = []

            if not row_index == 0:
                surrounding_entries.append(lines[row_index - 1][col_index])
            if not row_index == len(lines) - 1:
                surrounding_entries.append(lines[row_index + 1][col_index])
            if not col_index == 0:
                surrounding_entries.append(line[col_index - 1])
            if not col_index == len(line) - 1:
                surrounding_entries.append(line[col_index + 1])

            if entry < min(surrounding_entries):
                low_points.append((int(entry), row_index, col_index))
    return low_points


def challenge_one(lines: List[List[str]]) -> int:
    """Wraps up steps for challenge one"""
    low_points = get_low_points(lines)
    return sum(x[0] + 1 for x in low_points)


def get_neighbours(row_index, col_index, lines):
    """Helper - find non 9 neighbours of a point"""
    neighbours = []
    line = lines[row_index]
    if not row_index == 0:
        point = int(lines[row_index - 1][col_index])
        if point != 9:
            neighbours += [(point, row_index - 1, col_index)]
    if not row_index == len(lines) - 1:
        point = int(lines[row_index + 1][col_index])
        if point != 9:
            neighbours += [(point, row_index + 1, col_index)]

    if not col_index == 0:
        point = int(line[col_index - 1])
        if point != 9:
            neighbours += [(point, row_index, col_index - 1)]

    if not col_index == len(line) - 1:
        point = int(lines[row_index][col_index + 1])
        if point != 9:
            neighbours += [(point, row_index, col_index + 1)]
    return neighbours


def calculate_basin_size(point, row_index, col_index, lines):
    """Starts a walk from the initial point. Whilst there are neighbors to explore, for each point:
        * Find neighbors of that point (that don't have a value of 9)
        * Adds those that are unexplored to a list of neighbors to visit
        * Records that an entry has been visited

    Returns a list of points visited before the neighbor set was exhausted
    """
    entries = [(point, row_index, col_index)]
    neighbors = get_neighbours(row_index=row_index, col_index=col_index, lines=lines)
    while len(neighbors) > 0:
        new_point, new_row_index, new_col_index = neighbors.pop()
        entries.append((new_point, new_row_index, new_col_index))
        new_neighbors = get_neighbours(row_index=new_row_index, col_index=new_col_index, lines=lines)
        new_neighbors = list((set(new_neighbors) - set(entries) - set(entries)))

        neighbors.extend(new_neighbors)

    return len(set(entries))  # Set should be unnecessary


def get_basin_sizes(lines: List[List[str]], low_points: List[Tuple[int, int, int]]) -> List[int]:
    """Helper to calculate basin sizes for each low point"""
    basin_sizes = []
    for point, row_index, col_index in low_points:
        basin_size = calculate_basin_size(point, row_index, col_index, lines)
        basin_sizes.append(basin_size)
    return basin_sizes


def challenge_two(lines: List[List[str]]) -> int:
    """Wrap up steps for challenge two"""
    low_points = get_low_points(lines)
    basin_sizes = get_basin_sizes(lines, low_points)
    basin_sizes.sort()
    top_basins = basin_sizes[len(basin_sizes) - 3 :]

    return prod(top_basins)


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day9.txt"
    input_lines = setup_game(filepath=FILEPATH)

    # Challenge one
    challenge_one = challenge_one(lines=input_lines)
    print(f"Challenge one: {challenge_one}")

    # Challenge two
    challenge_two = challenge_two(lines=input_lines)
    print(f"Challenge two: {challenge_two}")
