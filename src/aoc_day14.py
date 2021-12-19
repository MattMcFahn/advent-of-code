"""Solutions to day 14"""
from typing import Dict
from collections import Counter
from math import ceil


def setup_game(filepath: str) -> (Counter, Dict[str, str]):
    """
    From the input filepath, reads the input sequence, and rules
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [x.strip("\n") for x in lines]

    start_sequence = lines[0]
    pairs = Counter([start_sequence[i : i + 2] for i in range(0, len(start_sequence) - 1)])
    rules = {x[:2]: x[-1] for x in lines if "->" in x}

    return pairs, rules


def perform_step(sequence: Counter, rules: Dict[str, str]) -> Counter:
    """Performs a single step as described in the challenge"""
    new_sequence = Counter()
    for item, value in sequence.items():
        new_entry_one = item[0] + rules[item]
        new_entry_two = rules[item] + item[1]
        new_sequence[new_entry_one] += value
        new_sequence[new_entry_two] += value

    return new_sequence


def sequence_to_step(start_sequence: Counter, rules: Dict[str, str], target_step: int) -> Counter:
    """Modifies the sequence until the target step, and gets the diff of max and min frequencies"""
    sequence = start_sequence
    for step in range(0, target_step):
        print(f"Step: {step + 1}")
        sequence = perform_step(sequence=sequence, rules=rules)

    return sequence


def single_letter_counter(sequence: Counter) -> Counter:
    """Helper that turns a counter of two letter occurrences to one letter occurrences"""
    counts = Counter()
    for key, value in sequence.items():
        counts[key[0]] += value / 2  # Bit of a hack - the most we'll be out is 0.5 down, so can ceil later
        counts[key[1]] += value / 2
    return counts


def challenge_one(start_sequence: Counter, rules: Dict[str, str]) -> int:
    """Completes challenge one"""
    new_sequence = sequence_to_step(start_sequence, rules, target_step=10)
    counts = single_letter_counter(new_sequence)
    return ceil(max(counts.values()) - min(counts.values()))


def challenge_two(start_sequence: str, rules: Dict[str, str]) -> int:
    """Completes challenge two"""
    new_sequence = sequence_to_step(start_sequence, rules, target_step=40)
    counts = single_letter_counter(new_sequence)
    return ceil(max(counts.values()) - min(counts.values()))


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day14.txt"
    input_sequence, input_rules = setup_game(filepath=FILEPATH)

    # Challenge one
    challenge_one = challenge_one(start_sequence=input_sequence, rules=input_rules)
    print(f"Challenge one: {challenge_one}")

    # Challenge two
    challenge_two = challenge_two(start_sequence=input_sequence, rules=input_rules)
    print(f"Challenge two: {challenge_two}")
