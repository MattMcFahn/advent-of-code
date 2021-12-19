"""Solutions to day 14"""
from typing import Dict
from collections import Counter


def setup_game(filepath: str) -> (str, Dict[str, str]):
    """
    From the input filepath, reads the input sequence, and rules
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [x.strip("\n") for x in lines]

    start_sequence = lines[0]
    rules = {x[:2]: x[-1] for x in lines if "->" in x}

    return start_sequence, rules


def perform_step(sequence: str, rules: Dict[str, str]) -> str:
    """Performs a single step as described in the challenge"""
    new_sequence = sequence[0]
    for index in range(0, len(sequence) - 1):
        chars = sequence[index : index + 2]
        new_sequence += rules[chars] + chars[-1]

    return new_sequence


def challenge_one(start_sequence: str, rules: Dict[str, str]) -> int:
    """Completes challenge one"""
    steps = 10
    sequence = start_sequence
    for step in range(0, steps):
        print(f"Step: {step + 1}")
        sequence = perform_step(sequence=sequence, rules=rules)

    counts = Counter(sequence)
    return max(counts.values()) - min(counts.values())


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day14.txt"
    input_sequence, input_rules = setup_game(filepath=FILEPATH)

    # Challenge one
    challenge_one = challenge_one(start_sequence=input_sequence, rules=input_rules)
    print(f"Challenge one: {challenge_one}")

    # Challenge two
    # challenge_two = challenge_two(input_frame=frame, fold_instructions=folds)
    # print(f"Challenge two: {challenge_two}")
