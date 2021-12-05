"""Helper script to calculate results for AOC challenge, day 3"""
import pandas as pd

# pylint: disable=fixme,no-else-return
# TODO: Update with the working version
# TODO: Update the input file


def get_input_as_dataframe(filepath: str) -> pd.DataFrame:
    """Simple helper to get the input and wrangle to a dataframe"""
    with open(filepath) as file:
        lines = file.readlines()
        values = [line.rstrip() for line in lines]

    dataframe = pd.DataFrame({"values": values})
    dataframe = dataframe["values"].str.split(pat="", expand=True)
    dataframe = dataframe.drop(columns={0, len(dataframe.values[0][0]) + 1})
    return dataframe


def get_opposite(val: str) -> str:
    """Returns '1' for input of '0', else '0'.

    Assumes only '0' or '1' will be passed to it.
    """
    return "1" if val == "0" else "0"


def get_selector(dataframe, col, oxygen):
    """Helper"""
    mode = dataframe[col].mode()
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


def calculate(dataframe: pd.DataFrame):
    """Helper to apply logic"""
    gamma = ""
    epsilon = ""
    for col in dataframe.columns:
        gamma_bit = get_selector(dataframe, col, True)
        epsilon_bit = get_opposite(int(gamma_bit))
        gamma += gamma_bit
        epsilon += epsilon_bit

    result = int(gamma, base=2) * int(epsilon, base=2)
    return result


def calculate_oxygen_or_life(dataframe: pd.DataFrame, oxygen_or_life: bool = True) -> int:
    """Calculates the score based on whether it's for oxygen or life"""
    col = 0
    subset = dataframe.copy()

    while len(subset) > 1:
        col += 1
        selector = get_selector(subset, col, oxygen_or_life)
        subset = subset.loc[dataframe[col] == selector]
    subset = subset.reset_index(drop=True)

    result = "".join([str(x) for x in subset.values[0]])
    return int(result, base=2)


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day3.txt"

    # Challenge one
    input_dataframe = get_input_as_dataframe(FILEPATH)
    challenge_one = calculate(input_dataframe)
    print(f"Challenge one result: {challenge_one}")

    # Challenge two
    oxygen_result = calculate_oxygen_or_life(input_dataframe)
    life_result = calculate_oxygen_or_life(input_dataframe, False)

    print(f"Oxygen: {oxygen_result}")
    print(f"Life: {life_result}")

    print(f"Challenge two result: {oxygen_result * life_result}")
