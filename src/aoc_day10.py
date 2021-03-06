"""Solutions to day 10"""
from typing import List

import re

closing_parens = r"[\>\]\}\)]"


def get_closing_paren(paren: str) -> str:
    """Helper to get matching closing parens"""
    matchers = {"[": "]", "{": "}", "(": ")", "<": ">"}
    return matchers[paren]


def setup_game(filepath: str) -> List[List[str]]:
    """
    From the input filepath, read the input strings into a list of lists
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [x.strip("\n") for x in lines]

    return lines


def get_broken_and_incomplete_strings(lines):
    """Main logic for identifying which strings are broken / incomplete"""
    invalid_strings = []
    breaking_chars = []
    incomplete_strings = []

    for line in lines:
        original_line = line
        while len(line) > 0 and ("()" in line or "[]" in line or "{}" in line or "<>" in line):
            line = line.replace("()", "").replace("[]", "").replace("{}", "").replace("<>", "")

        if not len(set(line) & {"}", "]", ")", ">"}) == 0:
            invalid_strings.append(original_line)

            invalid_matches = re.search(closing_parens, line)
            breaking_chars.append(invalid_matches.group(0))
        else:
            incomplete_strings.append(line)

    return invalid_strings, breaking_chars, incomplete_strings


def challenge_one(lines):
    """Assumes lines are of even length"""
    breaking_chars = get_broken_and_incomplete_strings(lines)[1]
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    total = sum([scores[x] for x in breaking_chars])
    return total


def challenge_two(lines):
    """Same assumption as challenge one"""
    incomplete_strings = get_broken_and_incomplete_strings(lines)[2]
    completions = []
    for string in incomplete_strings:
        completion = "".join(get_closing_paren(x) for x in string)[::-1]
        completions.append(completion)

    score_map = {")": 1, "]": 2, "}": 3, ">": 4}
    scores = []
    for string in completions:
        score = 0
        for char in string:
            score *= 5
            score += score_map[char]
        scores.append(score)
    scores.sort()
    return scores[int((len(scores) - 1) / 2)]


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day10.txt"
    input_lines = setup_game(filepath=FILEPATH)

    # Challenge one
    challenge_one = challenge_one(input_lines)
    print(f"Challenge one: {challenge_one}")

    # Challenge two
    challenge_two = challenge_two(input_lines)
    print(f"Challenge two: {challenge_two}")
