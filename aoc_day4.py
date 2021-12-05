"""A python solution to Advent of Code day 4 challenges"""
from typing import Union, Dict, List

import pandas as pd
import numpy as np

# pylint: disable=fixme
# TODO: Update with the working version from other machine
# TODO: Add input file


def setup_game(filepath: str) -> Union[List, Dict[int, pd.DataFrame]]:
    """
    From the input filepath, creates a list of integers to be called in order,
    and the three boards for the game

    """
    with open(filepath) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    numbers = [int(x) for x in lines[0].split(",")]
    lines = lines[2:]

    boards = {}
    for i in [1, 2, 3]:
        relevant_lines = [[int(x) for x in y.split(" ") if x != ""] for y in lines[:5]]
        board = pd.DataFrame({i: relevant_lines[i] for i in range(0, 5)}).T
        boards[i] = board
        lines = lines[6:]

    return numbers, boards


def check_verticals(board, numbers):
    """Implements the vertical checks of check_board_won"""
    for i in range(0, len(board)):  # pylint: disable=consider-using-enumerate
        values = set(board[i].values)
        if not values - set(numbers):
            return True
    return False


def check_horizontals(board, numbers):
    """Implements the horizontal checks of check_board_won"""
    return check_verticals(board.T, numbers)


def check_diagonals(board, numbers):
    """Implements the diagonal checks of check_board_won"""
    diag_one = set(np.diag(board))
    diag_two = set(np.diag(board))

    return not diag_one - set(numbers) or not diag_two - set(numbers)


def check_board_won(board, numbers):
    """Checks whether a selection of numbers (>5) completes a board.
    Rules that ensure a board will be complete:
        * A diagonal line
        * A horizontal line
        * A vertical line
    """
    return (
        check_verticals(board, numbers)
        or check_horizontals(board, numbers)
        or check_diagonals(board, numbers)  # pylint: disable=line-too-long
    )


def get_winning_board(boards, numbers):
    """Returns winning board and last number added to win"""
    i = 5
    input_length = len(numbers)
    while i <= input_length:
        cut_numbers = numbers[:i]
        for board in boards.values():
            if check_board_won(board, numbers):
                winning_board = board
                winning_number = cut_numbers[-1]
        i += 1
    return winning_board, winning_number


if __name__ == "__main__":
    FILEPATH = r"resources/aoc-day4-TEST.txt"
    input_numbers, input_boards = setup_game(FILEPATH)
    final_board, final_number = get_winning_board(input_boards, input_numbers)
