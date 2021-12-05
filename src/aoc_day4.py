"""A python solution to Advent of Code day 4 challenges"""
from typing import Tuple, Dict, List

import pandas as pd
import numpy as np


def setup_game(filepath: str) -> Tuple[List, Dict[int, pd.DataFrame]]:
    """
    From the input filepath, creates a list of integers to be called in order,
    and the three boards for the game
    """
    with open(filepath) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    input_numbers = [int(x) for x in lines[0].split(",")]
    lines = lines[2:]

    input_boards = {}
    i = 0
    while len(lines) > 0:
        i += 1
        relevant_lines = [[int(x) for x in y.split(" ") if x != ""] for y in lines[:5]]
        board = pd.DataFrame({i: relevant_lines[i] for i in range(0, 5)}).T
        input_boards[i] = board
        lines = lines[6:]

    return input_numbers, input_boards


def check_verticals(board, input_numbers):
    """Implements the vertical checks of check_board_won"""
    for i in range(0, len(board)):
        values = set(board[i].values)
        if not values - set(input_numbers):
            return True
    return False


def check_horizontals(board, input_numbers):
    """Implements the horizontal checks of check_board_won"""
    return check_verticals(board.T, input_numbers)


def check_diagonals(board, input_numbers):
    """Implements the diagonal checks of check_board_won"""
    diag_one = set(np.diag(board))
    diag_two = set(np.diag(board))

    return not diag_one - set(input_numbers) or not diag_two - set(input_numbers)


def check_board_won(board, input_numbers):
    """Checks whether a selection of numbers (>5) completes a board.
    Rules that ensure a board will be complete:
        * A diagonal line
        * A horizontal line
        * A vertical line
    """
    return (
        check_verticals(board, input_numbers)
        or check_horizontals(board, input_numbers)
        or check_diagonals(board, input_numbers)
    )


def get_winning_board(input_boards: Dict[int, pd.DataFrame], input_numbers: List[int]) -> Tuple[pd.DataFrame, List]:
    """Returns winning board, and the numbers called up till that point"""
    i = 5
    input_length = len(input_numbers)

    while i <= input_length:
        cut_numbers = input_numbers[:i]
        for board in input_boards.values():
            if check_board_won(board, cut_numbers):
                winning_board = board
                return winning_board, cut_numbers
        i += 1
    return Exception("No winning board found - check code")


def get_losing_board(input_boards: Dict[int, pd.DataFrame], input_numbers: List[int]) -> Tuple[pd.DataFrame, List]:
    """Returns the LAST board that would win, and the numbers called up till that point"""
    input_length = len(input_numbers)
    i = len(input_numbers)

    while i >= 5:
        cut_numbers = input_numbers[:i]
        for board in input_boards.values():
            if not check_board_won(board, cut_numbers):
                losing_board = board
                return losing_board, input_numbers[: i + 1]
        i -= 1
    return Exception("No losing board found - check code")


def get_unmarked_number_total(winning_board: pd.DataFrame, input_numbers: List):
    """Returns the sum of all numbers on winning_board that aren't in numbers"""
    values = []
    for x in winning_board.columns:
        values.extend([y for y in winning_board[x].to_list()])

    non_marked_number_set = set(values) - set(input_numbers)
    non_marked_numbers = [x for x in values if x in non_marked_number_set]
    return sum(non_marked_numbers)


def challenge_one(input_numbers: List, input_boards: Dict[int, pd.DataFrame]):
    """Chain steps for challenge 1 - get the winning board, and have sum of unmarked numbers * winning number"""
    winning_board, winning_numbers = get_winning_board(input_boards, input_numbers)
    winning_number = winning_numbers[-1]

    unmarked_number_total = get_unmarked_number_total(winning_board, winning_numbers)
    result = unmarked_number_total * winning_number
    return result


def challenge_two(input_numbers: List, input_boards: Dict[int, pd.DataFrame]):
    """Chain steps for challenge 2 - get the LAST board to win, and sum unmarked numbers * winning number"""
    losing_board, losing_numbers = get_losing_board(input_boards, input_numbers)
    winning_number = losing_numbers[-1]

    unmarked_number_total = get_unmarked_number_total(losing_board, losing_numbers)
    result = unmarked_number_total * winning_number
    return result


if __name__ == "__main__":
    FILEPATH = r"/resources/aoc-day4.txt"
    numbers, boards = setup_game(FILEPATH)

    challenge_one_result = challenge_one(numbers, boards)
    print(f"Challenge one: {challenge_one_result}")

    challenge_two_result = challenge_two(numbers, boards)
    print(f"Challenge two: {challenge_two_result}")
