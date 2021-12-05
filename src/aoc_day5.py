"""Script for day 5 solution"""
from typing import Dict, List, Tuple

import math
import numpy as np

# pylint: disable=fixme
# TODO: Align line length for black and pylint


def setup_game(filepath: str) -> List[Dict[str, Tuple]]:
    """

    From the input filepath, creates a list of integers to be called in order,
    and the three boards for the game
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [x.strip("\n") for x in lines]

    values = [
        {
            "x": (int(x[: x.find(",")]), int(x[x.rfind("-> ") + 3 : x.rfind(",")])),
            "y": (int(x[x.find(",") + 1 : x.find("->") - 1]), int(x[x.rfind(",") + 1 :])),
        }
        for x in lines
    ]

    return values


def setup_zero_board(value_list: List[Dict[str, Tuple]]) -> np.array:
    """Gets max x and y values, and creates an empty array of size max_x * max_y"""
    max_x = max(
        list(values["x"][0] for values in input_values)
        + list(values["x"][1] for values in value_list)  # pylint: disable=line-too-long
    )
    max_y = max(
        list(values["y"][0] for values in input_values)
        + list(values["y"][1] for values in value_list)  # pylint: disable=line-too-long
    )
    maximum = max(max_x, max_y)
    return np.zeros(shape=(maximum + 1, maximum + 1))


def is_horizontal_or_vertical(line: Dict[str, Tuple]) -> bool:
    """Is this line going horizontally or vertically"""
    return len(set(line["x"])) == 1 or len(set(line["y"])) == 1


def get_degrees(start_point, end_point):
    """

    Helper to get degrees between two points.
    Used to determine the orientation of a line between the points
    """
    return math.degrees(math.atan2(start_point[1] - end_point[1], start_point[0] - end_point[0]))


def get_points_crossed(line: Dict[str, Tuple]) -> List[Tuple]:
    """
    Identify points crossed by a line. For diagonals, verifies that the angle is 45 degrees by
    checking that the length traveled in each co-ordinate direction is equal
    """
    if len(set(line["x"])) == 1:
        x_coordinate = line["x"][0]
        y_values = range(min(line["y"]), max(line["y"]) + 1)

        points = list(zip([x_coordinate] * len(y_values), y_values))

    if len(set(line["y"])) == 1:
        y_coordinate = line["y"][0]
        x_values = range(min(line["x"]), max(line["x"]) + 1)

        points = list(zip(x_values, [y_coordinate] * len(x_values)))

    elif not len(set(line["y"])) == 1 and not len(set(line["x"])) == 1:
        start_index = 0 if line["x"][0] < line["x"][1] else 1
        end_index = int(not start_index)
        start_point = (line["x"][start_index], line["y"][start_index])
        end_point = (line["x"][end_index], line["y"][end_index])

        if get_degrees(start_point, end_point) == 135:
            points = [
                (coord, start_point[1] - step)
                for coord, step in zip(
                    range(start_point[0], end_point[0] + 1),
                    range(0, len(range(start_point[0], end_point[0] + 1)) + 1),  # pylint: disable=line-too-long
                )
            ]
        elif get_degrees(start_point, end_point) == -135:
            points = [
                (coord, start_point[1] + step)
                for coord, step in zip(
                    range(start_point[0], end_point[0] + 1),
                    range(0, len(range(start_point[0], end_point[0] + 1)) + 1),  # pylint: disable=line-too-long
                )
            ]

    return points


def mark_board(board: np.array, points: List[Tuple]) -> np.array:
    """Add +1 to each point crossed"""
    for point in points:
        # -1 is due to indexing at 0 for a numpy array
        board[point[1], point[0]] += 1
    return board


def update_board(
    board: np.array, values: List[Dict[str, tuple]], diagonals: bool = False
) -> np.array:  # pylint: disable=line-too-long
    """

    Given the input co-ordinates and starting board, identify horizontal / vertical lines,
    and update the board with points that have been crossed
    """
    for line in values:
        if is_horizontal_or_vertical(line):
            points = get_points_crossed(line)
            board = mark_board(board, points)
        else:
            if diagonals:
                points = get_points_crossed(line)
                board = mark_board(board, points)

    return board


def get_number_points_greater_than_x(board: np.array, limit: int) -> int:
    """Given a numpy array and an input integer, count the number of entries > limit"""
    return (board >= limit).sum()


def challenge_one(values: List[Dict[str, tuple]], board: np.array) -> int:
    """Wraps up steps for challenge 1"""
    board = update_board(board, values, diagonals=False)
    return get_number_points_greater_than_x(board, limit=2)


def challenge_two(values: List[Dict[str, tuple]], board: np.array) -> int:
    """Wrap up steps for challenge 2"""
    board = update_board(board, values, diagonals=True)
    return get_number_points_greater_than_x(board, limit=2)


if __name__ == "__main__":
    FILEPATH = r"/resources/aoc-day5.txt"
    # Setup
    input_values = setup_game(FILEPATH)
    zero_board = setup_zero_board(input_values)

    # Challenge one
    board_one = zero_board.copy()
    challenge_one = challenge_one(input_values, board_one)
    print(f"Challenge one: {challenge_one}")

    # Challenge two
    board_two = zero_board.copy()
    challenge_two = challenge_two(input_values, board_two)
    print(f"Challenge two: {challenge_two}")
