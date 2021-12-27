"""Solutions to day 18"""
from typing import Dict, List, Union
from itertools import product
from math import ceil, floor
from ast import literal_eval

import re


class Pair:
    def __init__(self, string: str, parent, depth: int = 0):
        self.string = string
        self.list = literal_eval(string)
        self.parent = parent
        self.depth = depth
        self.root_depth = depth

        left = self.list[0]
        right = self.list[1]

        if type(left) == int:
            self.left = left
        else:
            self.left = Pair(string=str(left), parent=self, depth=depth + 1)
        if type(right) == int:
            self.right = right
        else:
            self.right = Pair(string=str(right), parent=self, depth=depth + 1)

        self.set_max_depth()

    def get_max_depth(self):
        if type(self.left) == int and type(self.right) == int:
            return self.depth + 1
        if type(self.left) == int:
            return self.right.get_max_depth()
        if type(self.right) == int:
            return self.left.get_max_depth()
        else:
            return max(self.left.get_max_depth(), self.right.get_max_depth())

    def set_max_depth(self):
        self.max_depth = self.get_max_depth()

    def get_explosion_pair(self):
        """Identifies the pair on which an explosion should happen"""
        if not self.max_depth >= 5:
            pass
        else:
            current_pair = self
            target_depth = current_pair.max_depth
            while not (type(current_pair.left) == int and type(current_pair.right) == int):
                print(target_depth)
                if type(current_pair.left) == int and not type(current_pair.right) == int:
                    print("Going right")
                    print(current_pair.right.list)
                    current_pair = current_pair.right
                    target_depth -= 1

                elif current_pair.left.get_max_depth() - current_pair.root_depth == target_depth:
                    print("Going left")
                    print(current_pair.left.list)
                    current_pair = current_pair.left
                    target_depth -= 1
                else:
                    print("Going right - final try")
                    print(current_pair.right.list)
                    current_pair = current_pair.right
                    target_depth -= 1

        return current_pair

    def apply_explosion(self, explosion_pair):
        """Applies an explosion. Bit hacky, uses the string and ONLY updates the string"""
        left_value = explosion_pair.list[0]
        right_value = explosion_pair.list[1]

        explosion_string = explosion_pair.string.replace(" ", "")
        position = self.string.find(explosion_string)
        start_string = self.string[:position]
        end_string = self.string[position + len(explosion_string) :]

        try:
            right_number = re.findall("[0-9]+", start_string)[-1]
            intermediate = start_string.rsplit(right_number, 1)
            intermediate[0][:-1]
            start_string = str(left_value + int(right_number)).join(intermediate)
        except:
            pass

        try:
            left_number = re.findall("[0-9]+", end_string)[0]
            intermediate = end_string.split(left_number, 1)
            end_string = str(right_value + int(left_number)).join(intermediate)
        except:
            pass

        new_string = start_string + "0" + end_string
        self.string = new_string

    def needs_split(self):
        """Does this pair type need a split"""
        numbers = [x for x in re.findall("[0-9]+", self.string) if int(x) > 9]
        return bool(numbers)

    def apply_split(self):
        """Applies a split. ONLY updates the string"""
        numbers = [x for x in re.findall("[0-9]+", self.string) if int(x) > 9]
        if numbers:
            number = numbers[0]
            self.string = self.string.replace(number, f"[{floor(int(number)/2)},{ceil(int(number)/2)}]")


def setup_game(filepath: str) -> List[Pair]:
    """
    From the input filepath, reads the input instructions.
    """
    with open(filepath) as file:
        lines = file.readlines()

    pair_list = []
    for x in lines:
        x = x.strip("\n")
        pair = Pair(string=x, parent=None, depth=0)
        pair_list.append(pair)

    return pair_list


def challenge_one(instructions: List[Pair]) -> int:
    """Completes challenge one"""
    final_sum_pair = instructions[0]
    for new_instruction in instructions[1:]:
        final_sum_string = "[" + final_sum_pair.string + "," + new_instruction.string + "]"
        final_sum_pair = Pair(string=final_sum_string, parent=None, depth=0)
        while final_sum_pair.max_depth >= 5 or final_sum_pair.needs_split():
            if final_sum_pair.max_depth >= 5:
                explosion_pair = final_sum_pair.get_explosion_pair()
                final_sum_pair.apply_explosion(explosion_pair=explosion_pair)

                new_string = final_sum_pair.string
            else:
                final_sum_pair.apply_split()
                new_string = final_sum_pair.string

            print(f"New string: {new_string}")
            final_sum_pair = Pair(string=new_string, parent=None, depth=0)

    return final_sum_pair


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day18-TEST.txt"
    print("Setup game... ")
    input_instructions = setup_game(filepath=FILEPATH)
    print("Setup game... DONE")

    # Challenge one
    print("Running challenge one...")
    challenge_one = challenge_one(instructions=input_instructions)
    # print(f"Challenge one: {challenge_one}")
