"""Solutions to day 24"""
from typing import List, Dict
from itertools import product, groupby
from math import floor
from datetime import datetime


def setup_game(filepath: str) -> List[str]:
    """
    From the input filepath, reads the input cube
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [x.strip("\n") for x in lines]

    positions = [idx for idx, element in enumerate(lines) if "inp " in element]

    instructions = [
        lines[value : positions[idx + 1]] for idx, value in enumerate(positions) if idx != len(positions) - 1
    ] + [lines[positions[len(positions) - 1] :]]

    return instructions


def get_game_setup_dict():
    """Helpful fixture"""
    return {"x": 0, "y": 0, "z": 0, "w": 0}


def number_generator(length):
    """Helpful name for a generator of numbers of specified 'length', with each digit in 1 through 9"""
    return product(*[range(9, 0, -1)] * length)


def apply_instruction(game, number, instruction):
    """Apply a single instruction"""
    if instruction[0] == "inp" and instruction[1] == "w":
        game["w"] = number
    else:
        operator = instruction[2]
        if operator.strip("-").isnumeric():
            operator = int(operator)
        else:
            operator = game[operator]

    if instruction[0] == "add":
        game[instruction[1]] += operator

    if instruction[0] == "mul":
        game[instruction[1]] *= operator

    if instruction[0] == "div":
        game[instruction[1]] = floor(game[instruction[1]] / operator)

    if instruction[0] == "mod":
        game[instruction[1]] = game[instruction[1]] % operator

    if instruction[0] == "eql":
        game[instruction[1]] = int(game[instruction[1]] == operator)

    return game


def apply_game_logic(number_tuple, instructions):
    """Main logic for applying the MONAD instructions to a given number"""
    game = get_game_setup_dict()
    for index, instruction_list in enumerate(instructions):
        for instruction in instruction_list:
            instruction = instruction.split(" ")
            number = number_tuple[index]
            game = apply_instruction(game, number, instruction)

    return game


def number_is_valid(game):
    """"""
    return not (game["z"])


def challenge_one(instructions: List[str]) -> int:
    """Solves challenge one"""
    print(
        f"Running game on all 14 digit possible numbers, from highest backwards. "
        f"There are {9**14} to consider, so this wont terminate easily..."
    )
    max_number = 0
    length = len(instructions)
    while not max_number:
        for _, number_tuple in enumerate(number_generator(length)):
            # Hacky reporting on progress...
            if _ % 100000 == 0:
                print(f"{datetime.now()} Numbers considered: {_}")
                print(f"{datetime.now()} Current highest valid number: {max_number}")

            game = apply_game_logic(number_tuple, instructions)
            valid = number_is_valid(game)
            number = int("".join(str(a) for a in number_tuple))
            if number > max_number and valid:
                print(f"Max number found! {number}")
                max_number = number

    return max_number


def test_input_instruction_equality(instructions) -> List[bool]:
    """Helper to identify diffs"""
    equalities = []
    for i in range(0, len(instructions[0])):
        group = groupby([instructions[j][i] for j in range(0, len(instructions))])
        equality = next(group, True) and not next(group, False)
        equalities.append(equality)
    return equalities


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day24.txt"
    print(f"{datetime.now()} Setting up game... ")
    input_instructions = setup_game(filepath=FILEPATH)
    print(f"{datetime.now()} Setting up game... DONE")

    # Check on equalities
    input_equalities = test_input_instruction_equality(instructions=input_instructions)
    print("The only elements that differ in the inputs are...")
    for _, boolean in enumerate(input_equalities):
        if not boolean:
            print(f"Instruction: {_ + 1}")
    # Challenge one
    # print(f"{datetime.now()} Running challenge one... ")
    # challenge_one = challenge_one(instructions=input_instructions)
    # print(f"Challenge one: {challenge_one}")

    # # Challenge two
    # challenge_two = challenge_two(instructions=input_instructions)
    # print(f"Challenge one: {challenge_two}")
    #
