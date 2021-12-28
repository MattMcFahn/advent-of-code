"""Solutions to day 18"""
from typing import List
from math import ceil, floor
from ast import literal_eval

import re

# pylint: disable=too-many-instance-attributes, no-else-return


class Pair:
    """Custom class for a pair element, which has a left and right attribute, each of which is either an int or a Pair
    itself"""

    def __init__(self, string: str, parent, depth: int = 0):
        self.string = string
        self.list = literal_eval(string)
        self.parent = parent
        self.depth = depth
        self.root_depth = depth

        left = self.list[0]
        right = self.list[1]

        if isinstance(left, int):
            self.left = left
        else:
            self.left = Pair(string=str(left), parent=self, depth=depth + 1)
        if isinstance(right, int):
            self.right = right
        else:
            self.right = Pair(string=str(right), parent=self, depth=depth + 1)

        self.set_max_depth()

    def get_max_depth(self):
        """Helper to get a max node depth for a pair"""
        if isinstance(self.left, int) and isinstance(self.right, int):
            return self.depth + 1
        if isinstance(self.left, int):
            return self.right.get_max_depth()
        if isinstance(self.right, int):
            return self.left.get_max_depth()
        else:
            return max(self.left.get_max_depth(), self.right.get_max_depth())

    def set_max_depth(self):
        """Used to initialise the max depth in the __init__"""
        self.max_depth = self.get_max_depth()

    def get_explosion_pair(self):
        """Identifies the pair on which an explosion should happen"""
        if not self.max_depth >= 5:
            pass
        else:
            current_pair = self
            target_depth = current_pair.max_depth
            while not (isinstance(current_pair.left, int) and isinstance(current_pair.right, int)):
                if isinstance(current_pair.left, int) and not isinstance(current_pair.right, int):
                    current_pair = current_pair.right
                    target_depth -= 1

                elif current_pair.left.get_max_depth() - current_pair.root_depth == target_depth:
                    current_pair = current_pair.left
                    target_depth -= 1
                else:
                    current_pair = current_pair.right
                    target_depth -= 1

        return current_pair

    def apply_explosion(self, explosion_pair):
        """Applies an explosion. Bit hacky, uses the string and ONLY updates the string"""
        prefix = self.string[: self.string.find(explosion_pair.parent.string.replace(" ", ""))]
        other = self.string[self.string.find(explosion_pair.parent.string.replace(" ", "")) :]

        left_value = explosion_pair.list[0]
        right_value = explosion_pair.list[1]

        explosion_string = explosion_pair.string.replace(" ", "")
        position = other.find(explosion_string)

        start_string = other[:position]
        end_string = other[position + len(explosion_string) :]

        try:
            right_number = re.findall("[0-9]+", start_string)[-1]
            intermediate = start_string.rsplit(right_number, 1)
            start_string = str(left_value + int(right_number)).join(intermediate)
            left_done = True
        except IndexError:
            left_done = False

        if not left_done:
            try:
                right_number = re.findall("[0-9]+", prefix)[-1]
                intermediate = prefix.rsplit(right_number, 1)
                prefix = str(left_value + int(right_number)).join(intermediate)
            except IndexError:
                pass

        start_string = prefix + start_string

        try:
            left_number = re.findall("[0-9]+", end_string)[0]
            intermediate = end_string.split(left_number, 1)
            end_string = str(right_value + int(left_number)).join(intermediate)
        except IndexError:
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
            print(f"Split: {number}")
            self.string = self.string.replace(number, f"[{floor(int(number)/2)},{ceil(int(number)/2)}]", 1)


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


def get_final_pair(instructions: List[Pair]) -> Pair:
    """Main logic that applies snailfish addition"""
    final_sum_pair = instructions[0]
    new_string = final_sum_pair.string
    for new_instruction in instructions[1:]:
        print(f"New string: {new_string}")
        print("\n")
        final_sum_string = "[" + final_sum_pair.string + "," + new_instruction.string + "]"
        final_sum_pair = Pair(string=final_sum_string, parent=None, depth=0)
        print(f"New string after addition: {final_sum_pair.list}")
        while final_sum_pair.max_depth >= 5 or final_sum_pair.needs_split():
            if final_sum_pair.max_depth >= 5:
                explosion_pair = final_sum_pair.get_explosion_pair()
                print(f"Explosion pair: {explosion_pair.list}")
                final_sum_pair.apply_explosion(explosion_pair=explosion_pair)

                new_string = final_sum_pair.string
            else:
                final_sum_pair.apply_split()
                new_string = final_sum_pair.string

            print(f"New string: {new_string}")
            final_sum_pair = Pair(string=new_string, parent=None, depth=0)

    return final_sum_pair


def challenge_one(pair: Pair) -> int:
    """Wraps up challenge one"""
    string = pair.string
    while string.count(",") > 0:
        pairs = re.findall(r"\[\d+,\d+\]", string)
        replacements = {x: str(3 * int(x[1 : x.find(",")]) + 2 * int(x[x.find(",") + 1 : -1])) for x in pairs}
        for x, y in replacements.items():
            string = string.replace(x, y)
    return int(string)


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day18.txt"
    print("Setup game... ")
    input_instructions = setup_game(filepath=FILEPATH)
    print("Setup game... DONE")

    final_pair = get_final_pair(instructions=input_instructions)

    # Challenge one
    print("Running challenge one...")
    challenge_one = challenge_one(pair=final_pair)
    print(f"Challenge one: {challenge_one}")
