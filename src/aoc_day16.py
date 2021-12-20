"""
 Solutions to day 16 - hexidecimal/binary fun.
 Way too much reading for this problem...
"""
from typing import Dict, List


def setup_game(filepath: str) -> str:
    """
    From the input filepath, reads the input hexidecimal sequence, and parses into sections
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [x.strip("\n") for x in lines]

    return lines[0]


def hex_to_decimal(char: str) -> str:
    """Helper to convert to decimal"""
    return {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }[char]


def get_binary_string(hex_string: str) -> str:
    """Helper that turns the hex string into a list of binary chars"""
    return "".join([hex_to_decimal(char) for char in hex_string])


def get_chunk_length_or_number_of_packets(binary_string: str, length_type_id: str) -> int:
    """Helper to find out the length of chunks, or number of packets"""
    length_chunk = binary_string[7:22] if length_type_id == "0" else binary_string[7:18]
    return int(length_chunk, 2)


def handle_literal(binary_string: str) -> (str, int):
    """Logic to handle a literal in chunks of 5"""
    version = binary_string[:3]
    type_id = binary_string[3:6]
    length_type_id = binary_string[6]

    for number in range(7, len(binary_string), 5):
        chunk = binary_string[number - 1 : number - 1 + 4]
        if chunk[0] == "0":
            binary_string = binary_string[number:]
    return int(version, 2), binary_string


def collect_packet_versions(binary_string: str) -> List[int]:
    """"""
    packet_versions = []

    while binary_string != "" and not set(binary_string) == {"0"}:
        packet_version = binary_string[:3]
        packet_versions.append(int(packet_version, 2))

        packet_type_id = binary_string[3:6]
        length_type_id = binary_string[6]
        # if length_type_id =
        # chunk_length = get_chunk_length_or_number_of_packets(binary_string=binary_string, length_type_id=length_type_id)

        # If packet type id is 4, it's a literal so we need different logic
        if packet_type_id == "4":
            print("Literal packet being handled")
            binary_string, literal_version = handle_literal(binary_string)
            print(f"Literal version: {literal_version}")
            packet_versions.append(literal_version)

        else:
            binary_string = binary_string[22:] if length_type_id == "0" else binary_string[18:]
    return packet_versions


def challenge_one(hex_string: str) -> int:
    """Completes challenge one"""
    binary_string = get_binary_string(hex_string=hex_string)

    packet_versions = collect_packet_versions(binary_string=binary_string)
    return sum(packet_versions)


def challenge_two():
    """Completes challenge two"""
    return


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day16-TEST.txt"
    input_string = setup_game(filepath=FILEPATH)

    # Challenge one
    challenge_one = challenge_one(hex_string=input_string)
    print(f"Challenge one: {challenge_one}")

    # # Challenge two
    # challenge_two = challenge_two(start_sequence=input_sequence, rules=input_rules)
    # print(f"Challenge two: {challenge_two}")
