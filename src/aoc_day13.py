"""Solutions to day 13"""
from typing import List
import numpy as np
import pandas as pd

# pylint: disable=unnecessary-comprehension


def setup_game(filepath: str) -> (pd.DataFrame, List[str]):
    """
    From the input filepath, sets up the transparent paper as a dataframe and gets a list of folds to perform in order
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [x.strip("\n") for x in lines]

    co_ordinates = [(int(x[: x.find(",")]), int(x[x.find(",") + 1 :])) for x in lines if x != "" and "fold" not in x]
    fold_instructions = [x[x.find("=") - 1 :] for x in lines if "fold" in x]

    input_frame = pd.DataFrame(np.zeros((max([x[1] for x in co_ordinates]) + 1, max([x[0] for x in co_ordinates]) + 1)))
    for co_ordinate in co_ordinates:
        input_frame.loc[co_ordinate[1]].iloc[co_ordinate[0]] = 1

    for column in input_frame.columns:
        input_frame[column] = input_frame[column] > 0

    return input_frame, fold_instructions


def horizontal_fold(dataframe: pd.DataFrame, position: int) -> pd.DataFrame:
    """Performs a horizontal fold, i.e. along y = y_0"""
    top_frame = dataframe.head(position)
    bottom_frame = dataframe.tail(position)
    bottom_frame = bottom_frame.sort_index(ascending=False).reset_index(drop=True)
    new_frame = top_frame + bottom_frame
    return new_frame


def vertical_fold(dataframe: pd.DataFrame, position: int) -> pd.DataFrame:
    """Performs a vertical fold, i.e. along x = x_0"""
    left_frame = dataframe[range(0, position)]
    right_frame = dataframe[range(position + 1, len(dataframe.columns))]
    right_frame = right_frame[right_frame.columns[::-1]]

    column_renames = {x: y for x, y in zip(right_frame.columns, range(0, len(right_frame)))}

    right_frame = right_frame.rename(columns=column_renames)

    new_frame = left_frame + right_frame
    return new_frame


def challenge_one(input_frame: pd.DataFrame, fold_instructions: List[str]) -> int:
    """Completes challenge one"""
    first_fold = fold_instructions[0]

    fold_functions = {"y": horizontal_fold, "x": vertical_fold}

    new_frame = fold_functions[first_fold[0]](
        dataframe=input_frame, position=int(first_fold[first_fold.find("=") + 1 :])
    )

    return new_frame.sum().sum()


def challenge_two(input_frame: pd.DataFrame, fold_instructions: List[str]) -> pd.DataFrame:
    """Completes challenge two - reading the letters is manual :("""
    final_frame = input_frame.copy()
    fold_functions = {"y": horizontal_fold, "x": vertical_fold}
    for fold in fold_instructions:
        final_frame = fold_functions[fold[0]](dataframe=final_frame, position=int(fold[fold.find("=") + 1 :]))
    return final_frame


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day13.txt"
    frame, folds = setup_game(filepath=FILEPATH)

    # Challenge one
    challenge_one = challenge_one(input_frame=frame, fold_instructions=folds)
    print(f"Challenge one: {challenge_one}")

    # # Challenge two
    challenge_two = challenge_two(input_frame=frame, fold_instructions=folds)
    # print(f"Challenge two: {challenge_two}")
