"""Solutions to day 8"""
from typing import List


def setup_game(filepath: str) -> List[str]:
    """
    From the input filepath, read and sort the input strings
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [list(x.strip("\n")) for x in lines]
    # frame = pd.DataFrame(lines)

    return lines


def get_low_points(lines: List[List[str]]) -> List[int]:
    """Helper to get low points with double enumerate - not the neatest"""
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
                low_points.append(int(entry))
    return low_points


def challenge_one(lines: List[List[str]]) -> int:
    """Wraps up steps for challenge one"""
    low_points = get_low_points(lines)

    return sum(x + 1 for x in low_points)


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day9.txt"
    input_lines = setup_game(filepath=FILEPATH)

    # Challenge one
    challenge_one = challenge_one(lines=input_lines)
    print(f"Challenge one: {challenge_one}")
    #
    # # Challenge two
    # challenge_two = challenge_two(lines=input_lines)
    # print(f"Challenge two: {challenge_two}")
