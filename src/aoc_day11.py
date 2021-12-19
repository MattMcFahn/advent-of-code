"""Solutions to day 11"""
from typing import List
import pandas as pd


def setup_game(filepath: str) -> List[List[str]]:
    """
    From the input filepath, read the input strings into a list
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [list(x.strip("\n")) for x in lines]
    frame = pd.DataFrame(lines)
    for col in frame.columns:
        frame[col] = frame[col].astype(int)

    return frame


def increment_frame(index, col_index, frame):
    """TODO: Increment the surrounding cells of frame"""
    surrounding_points = [
        (index - 1, col_index - 1),
        (index - 1, col_index),
        (index - 1, col_index + 1),
        (index + 1, col_index + 1),
        (index + 1, col_index),
        (index + 1, col_index - 1),
        (index, col_index - 1),
        (index, col_index + 1),
    ]
    surrounding_points = [
        x for x in surrounding_points if x[0] not in (-1, frame.shape[0]) and x[1] not in (-1, frame.shape[1])
    ]

    for point in surrounding_points:
        if not frame.loc[point[1]].iloc[point[0]] == 0:
            frame.loc[point[1]].iloc[point[0]] += 1

    return frame


def simulate_step(frame: pd.DataFrame, counter: int) -> (pd.DataFrame, int):
    """Simulates a single steps with rules specified"""
    frame += 1
    while max(frame.max()) > 9:
        for index, row in frame.iteritems():  # Row is really a column
            # print(f"Index: {index}")
            # print(f"Row: {row}")
            for col_index, value in row.iteritems():
                # print(f"Column: {col_index}")
                # print(f"Value: {value}")

                if value > 9:
                    counter += 1
                    frame.loc[col_index].iloc[index] = 0
                    frame = increment_frame(index, col_index, frame)

    return frame, counter


def simulate_to_given_step(frame: pd.DataFrame, counter: int, target_steps: int) -> (pd.DataFrame, int):
    """Simulate a dataframe and counter up until a given step"""
    for step in range(0, target_steps):
        print(f"Step: {step + 1}")
        frame, counter = simulate_step(frame, counter)
    return frame, counter


def challenge_one(frame: pd.DataFrame) -> int:
    """Wraps steps for challenge one"""
    target_steps = 100
    counter = 0
    frame, counter = simulate_to_given_step(frame, counter, target_steps)

    return counter


def challenge_two(frame: pd.DataFrame) -> int:
    """Steps for challenge two: walk through steps until max everywhere is 0"""
    step = 0
    counter = 0
    while max(frame.max()) > 0:
        step += 1
        print(f"Step: {step}")
        frame, counter = simulate_step(frame, counter)
    return step


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day11.txt"
    input_frame = setup_game(filepath=FILEPATH)
    challenge_one_frame = input_frame.copy()

    # Challenge one
    challenge_one = challenge_one(frame=challenge_one_frame)
    print(f"Challenge one: {challenge_one}")

    # Challenge two
    challenge_two_frame = input_frame.copy()
    challenge_two = challenge_two(frame=challenge_two_frame)
    print(f"Challenge two: {challenge_two}")
