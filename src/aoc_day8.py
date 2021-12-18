"""Solutions to day 8"""
from typing import List, Dict, Union, Tuple


def get_expected_mappings() -> Dict[int, List[str]]:
    """Fixture to set up the expected mappings of integers to lists of strings"""
    return {
        0: ["a", "b", "c", "e", "f", "g"],
        1: ["c", "f"],
        2: ["a", "c", "d", "e", "g"],
        3: ["a", "c", "d", "f", "g"],
        4: ["b", "c", "d", "f"],
        5: ["a", "b", "d", "f", "g"],
        6: ["a", "b", "d", "e", "f", "g"],
        7: ["a", "c", "f"],
        8: ["a", "b", "c", "d", "e", "f", "g"],
        9: ["a", "b", "c", "d", "f", "g"],
    }


def setup_game(filepath: str) -> List[str]:
    """
    From the input filepath, read and sort the input strings
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [x.strip("\n") for x in lines]

    # Sort strings
    lines = [x.split(" ") for x in lines]
    for index, line in enumerate(lines):
        line = lines[index]
        line = ["".join(sorted(x)) for x in line]
        line = " ".join(line)
        lines[index] = line

    return lines


def challenge_one(lines: List[str]) -> int:
    """Solution for challenge one"""
    unique_lengths = [2, 3, 4, 7]
    line = " ".join([x.split(" | ")[1] for x in lines])  # Get only outputs
    result = len([x for x in line.split(" ") if len(x) in unique_lengths])
    return result


def get_easy_patterns(entries) -> Dict[int, List[str]]:
    """Get the easy patterns"""
    patterns = dict()
    for key, length in {1: 2, 7: 3, 4: 4, 8: 7}.items():
        values = {x for x in entries if len(x) == length}

        if len(values) != 1:
            raise Exception(f"Issue identifying pattern for number: {key}")
        value = values.pop()
        value = list(value)
        patterns[key] = value
    return patterns


def setup_constraints(
    expected_mappings: Dict[int, List[str]], patterns: Dict[int, List[str]]
) -> Dict[Union[Tuple, str], Union[Tuple, str]]:
    """Identify two constraints that we'll use to identify which numbers are which patterns"""
    expected_patterns = {x: y for x, y in expected_mappings.items() if x in [1, 7, 4, 8]}

    constraints = {
        (expected_patterns[1][0], expected_patterns[1][1]): (patterns[1][0], patterns[1][1]),
        tuple(set(expected_patterns[4]) - set(expected_patterns[1])): tuple(set(patterns[4]) - set(patterns[1])),
    }

    # HACK: Ordering of ('b', 'd'), ('c', 'f')
    # TODO: Clean
    if ("b", "d") in constraints.keys():
        constraints[("d", "b")] = constraints[("b", "d")]
    if ("f", "c") in constraints.keys():
        constraints[("c", "f")] = constraints[("f", "c")]

    return constraints


def get_result_single_constraint(number: int, full_length: int, match_length: int, constraint: set, entries) -> str:
    """Helper that identifies which string must correspond to the given `number`,
    based on the constraint and match_length identified
    """
    result = {x for x in entries if len(x) == full_length and len(set(x) & constraint) == match_length}
    if len(result) != 1:
        raise Exception(f"Issue identifying pattern for number: {number}")

    result = result.pop()
    result = list(result)
    return result


def identify_six_entry_numbers(constraints, entries, patterns):
    """9, 0, 6"""
    # 9 is the only one with "expected" ('b', 'd'), ('c','f') in it
    constraint = set("".join(constraints[("d", "b")]).join(constraints[("c", "f")]))
    result = get_result_single_constraint(9, 6, 4, constraint, entries)
    patterns[9] = result

    # 0 has only one of "expected" ('b', 'd')
    constraint = set("".join(constraints[("d", "b")]))
    result = get_result_single_constraint(0, 6, 1, constraint, entries)
    patterns[0] = result

    # 6 has only one of "expected" ('c', 'f')
    constraint = set("".join(constraints[("c", "f")]))
    result = get_result_single_constraint(6, 6, 1, constraint, entries)
    patterns[6] = result
    return patterns


def identify_five_entry_numbers(constraints, entries, patterns):
    """2, 3, 5"""
    # 2 has EXACTLY one of the ('c', 'f') and ('d', 'b') tuples
    constraint_one = set("".join(constraints[("d", "b")]))
    constraint_two = set("".join(constraints[("c", "f")]))
    result = {
        x for x in entries if len(x) == 5 and len(set(x) & constraint_one) == 1 and len(set(x) & constraint_two) == 1
    }
    if len(result) != 1:
        raise Exception("Issue identifying pattern for number: 2")
    result = result.pop()
    result = list(result)
    patterns[2] = result

    # 3 must have "expected" ('c', 'f')
    constraint = set("".join(constraints[("c", "f")]))
    result = get_result_single_constraint(3, 5, 2, constraint, entries)
    patterns[3] = result

    # 5 has only one of "expected" ('b', 'd')
    constraint = set("".join(constraints[("d", "b")]))
    result = get_result_single_constraint(5, 5, 2, constraint, entries)
    patterns[5] = result
    return patterns


def get_hard_patterns(expected_mappings: Dict[int, List[str]], patterns: Dict[int, List[str]], entries: List[str]):
    """Identify those patterns that aren't immediately obvious:
        * Input sequences with 6 letters/entries
        * Input sequences with 5 letters/entries
    """
    # Other constraints identifiable from the 4 determinable - build a system of sim eqs
    constraints = setup_constraints(expected_mappings=expected_mappings, patterns=patterns)

    patterns = identify_six_entry_numbers(constraints=constraints, entries=entries, patterns=patterns)
    patterns = identify_five_entry_numbers(constraints=constraints, entries=entries, patterns=patterns)

    return patterns


def identify_patterns(line: str, expected_mappings: Dict[int, List[str]]) -> Dict[str, int]:
    """From an input list, identify which string sequences correspond to which integers"""
    entries = line.split(" ")
    entries.remove("|")
    entries = ["".join(sorted(x)) for x in entries]

    patterns = get_easy_patterns(entries=entries)
    patterns = get_hard_patterns(expected_mappings=expected_mappings, patterns=patterns, entries=entries)
    patterns = {"".join(y): x for x, y in patterns.items()}

    return patterns


def challenge_two(lines: List[str]) -> int:
    """Wrap up steps for challenge two. For each entry in our list:
        * Do analysis `identify_patterns` to map the input to corresponding numbers
        * Turn the last 4 output strings into the digits identified

    Then sum over all outputs
    """
    mappings = get_expected_mappings()
    results = []

    for line in lines:
        patterns = identify_patterns(line=line, expected_mappings=mappings)
        line.split(" | ")[1].split(" ")
        result = int("".join([str(patterns[x]) for x in line.split(" | ")[1].split(" ")]))
        results.append(result)

    return sum(results)


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day8.txt"
    input_lines = setup_game(filepath=FILEPATH)

    # Challenge one
    challenge_one = challenge_one(lines=input_lines)
    print(f"Challenge one: {challenge_one}")

    # Challenge two
    challenge_two = challenge_two(lines=input_lines)
    print(f"Challenge two: {challenge_two}")
