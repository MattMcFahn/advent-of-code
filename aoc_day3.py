"""Helper script to calculate results for AOC challenge, day 3"""
import pandas as pd

# pylint: disable=fixme
# TODO: Update with the working version
# TODO: Update the input file


def get_input_as_dataframe(filepath: str) -> pd.DataFrame:
    """Simple helper to get the input and wrangle to a dataframe"""
    with open(filepath) as file:
        lines = file.readlines()
        values = [line.rstrip() for line in lines]

    df = pd.DataFrame({"values": values})
    df = df["values"].str.split(pat="", expand=True).drop(columns={0, len(df.values[0][0]) + 1})
    return df


def get_opposite(val: str) -> str:
    """Returns '1' for input of '0', else '0'.

    Assumes only '0' or '1' will be passed to it.
    """
    return "1" if val == "0" else "0"


def get_selector(df, col, oxygen):
    """Helper"""
    mode = df[col].mode()
    if len(mode) > 1:
        if oxygen:
            return "1"
        else:
            return "0"
    else:
        mode = mode[0]
        if oxygen:
            return mode[0]
        else:
            return get_opposite(mode)


def calculate(df: pd.DataFrame):
    """Helper to apply logic"""
    gamma = ""
    epsilon = ""
    for col in df.columns:
        gamma_bit = get_selector(df, col, True)
        epsilon_bit = get_opposite(int(gamma_bit))
        gamma += gamma_bit
        epsilon += epsilon_bit

    result = int(gamma, base=2) * int(epsilon, base=2)
    return result


def calculate_oxygen_or_life(df: pd.DataFrame, oxygen_or_life: bool = True) -> int:
    """Calculates the score based on whether it's for oxygen or life"""
    col = 0
    subset = df.copy()

    while len(subset) > 1:
        col += 1
        selector = get_selector(subset, col, oxygen)
        subset = subset.loc[df[col] == selector]
    subset = subset.reset_index(drop=True)

    result = "".join([str(x) for x in subset.values[0]])
    return int(result, base=2)


if __name__ == "__main__":
    filepath = r"/resources/aoc-day3.txt"

    # Challenge one
    input_dataframe = get_input_as_dataframe(filepath)
    challenge_one = calculate(input_dataframe)
    print(f"Challenge one result: {challenge_one}")

    # Challenge two
    oxygen = calculate_oxygen_or_life(input_dataframe)
    life = calculate_oxygen_or_life(input_dataframe, False)

    print(f"Oxygen: {oxygen}")
    print(f"Life: {life}")

    print(f"Challenge two result: {oxygen * life}")
