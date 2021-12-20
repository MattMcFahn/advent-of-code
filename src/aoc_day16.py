"""
 Solutions to day 16 - hexidecimal/binary fun.
 Way too much reading for this problem...

"""
from typing import List
from collections import namedtuple
from math import prod

Packet = namedtuple("Packet", ("packet_version", "packet_type_id", "value", "sub_packets"))


def setup_game(filepath: str) -> str:
    """
    From the input filepath, reads the input hexadecimal sequence, and parses into sections
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [x.strip("\n") for x in lines]

    return lines[0]


def sum_packet_versions(packet: Packet) -> int:
    """Helper for a completed packet: get sum of packet_versions for all sub packets"""
    total = packet.packet_version
    for sub_packet in packet.sub_packets:
        total += sum_packet_versions(sub_packet)
    return total


def get_literal_value(binary_string: str, index: int) -> (int, int):
    """"""
    value = ""
    while True:
        last_group = binary_string[index] == "0"
        value += binary_string[(index + 1) : (index + 5)]
        index += 5
        if last_group:
            break
    return int(value, 2), index


def get_sub_packets_by_length(binary_string: str, index: int) -> (List[Packet], int):
    """"""
    sub_packets = []
    length_of_sub_packets = int(binary_string[index : index + 15], 2)
    index += 15
    length_used = 0
    while length_used < length_of_sub_packets:
        # Pass back to main handling, as may have literals or operators
        sub_packet, new_index = handle_string(binary_string, index)
        sub_packets.append(sub_packet)
        length_used += new_index - index
        index = new_index
    return sub_packets, index


def get_sub_packets_by_number(binary_string: str, index: int) -> (List[Packet], int):
    """"""
    sub_packets = []
    number_of_sub_packets = int(binary_string[index : index + 11], 2)
    index += 11
    for _ in range(number_of_sub_packets):
        # Pass back to main handling, as may have literals or operators
        sub_packet, index = handle_string(binary_string, index)
        sub_packets.append(sub_packet)
    return sub_packets, index


def handle_string(binary_string: str, index: int) -> (Packet, int):
    """Main entry point of recursion on any binary string:
        * Get packet packet_version
        * Get packet type id
        * If literal (type id = 4), handle literal, else
        * Get length_packet_type_id
        * Iteratively get sub packets by length (type id = "0") or number (type id = "1")
        * Get operator value
    """
    packet_version = int(binary_string[index : (index + 3)], 2)
    packet_type_id = int(binary_string[(index + 3) : (index + 6)], 2)
    index += 6
    if packet_type_id == 4:
        value, index = get_literal_value(binary_string, index)
        return Packet(packet_version, packet_type_id, value, []), index
    length_packet_type_id = binary_string[index]
    index += 1
    if length_packet_type_id == "0":
        sub_packets, index = get_sub_packets_by_length(binary_string, index)
    else:
        sub_packets, index = get_sub_packets_by_number(binary_string, index)
    value = calculate_value(packet_type_id, sub_packets)
    return Packet(packet_version, packet_type_id, value, sub_packets), index


def calculate_value(packet_type_id: int, sub_packets: List[Packet]) -> int:
    """"""
    value = 0
    function_map = {0: sum, 1: prod, 2: min, 3: max}
    if packet_type_id <= 3:
        values = (sub_packet.value for sub_packet in sub_packets)
        value = function_map[packet_type_id](values)
    else:
        sub_a, sub_b = sub_packets
        if packet_type_id == 5:
            value = sub_a.value > sub_b.value
        elif packet_type_id == 6:
            value = sub_a.value < sub_b.value
        elif packet_type_id == 7:
            value = sub_a.value == sub_b.value
        value = int(value)
    return value


def challenge_one(packet_object: Packet) -> int:
    """Completes challenge one"""
    return sum_packet_versions(packet_object)


def challenge_two(packet_object: Packet) -> int:
    """Completes challenge two"""
    return packet_object.value


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day16.txt"
    input_string = setup_game(filepath=FILEPATH)

    # Main logic, calculate Packet
    packet = handle_string(binary_string=bin(int(input_string, 16))[2:], index=0)[0]

    # Challenge one
    challenge_one = challenge_one(packet_object=packet)
    print(f"Challenge one: {challenge_one}")

    # Challenge two
    challenge_two = challenge_two(packet_object=packet)
    print(f"Challenge one: {challenge_two}")
