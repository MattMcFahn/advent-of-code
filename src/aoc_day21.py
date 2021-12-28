"""Solutions to day 21"""
from typing import Dict


def setup_game(filepath: str) -> Dict[int, Dict]:
    """
    From the input filepath, reads the input instructions.
    """
    with open(filepath) as file:
        lines = file.readlines()

    lines = [x.strip("\n") for x in lines]
    positions = {int(x[x.find("starting") - 2]): int(x[-1]) for x in lines}

    player_stats = {1: {"position": positions[1], "score": 0}, 2: {"position": positions[2], "score": 0}}

    return player_stats


def challenge_one(player_stats: Dict[int, Dict]) -> int:
    """Solves challenge one"""

    current_player = 1
    dice = 1
    rolls = 0
    while max(player_stats[1]["score"], player_stats[2]["score"]) < 1000:
        # Get movement, and update dice and total rolls
        move = dice + ((dice + 1) % 100) + ((dice + 2) % 100)
        dice = (dice + 3) % 100
        rolls += 3

        # Update players position
        player_stats[current_player]["position"] = (player_stats[current_player]["position"] + move - 1) % 10 + 1
        # Add position to score
        player_stats[current_player]["score"] += player_stats[current_player]["position"]

        # Swap player control
        current_player = current_player % 2 + 1

    min_score = min(player_stats[1]["score"], player_stats[2]["score"])

    print(f"Total rolls: {rolls}")
    print(f"Losing score: {min_score}")
    return rolls * min_score


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day21.txt"
    print("Setup game... ")
    input_player_stats = setup_game(filepath=FILEPATH)
    print("Setup game... DONE")

    # Challenge one
    print("Running challenge one...")
    challenge_one = challenge_one(player_stats=input_player_stats)
    print(f"Challenge one: {challenge_one}")
