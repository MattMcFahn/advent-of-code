"""Solutions to day 12"""
from typing import List, Dict
from collections import Counter


def setup_game(filepath: str) -> Dict[str, str]:
    """
    From the input filepath, reads the list of edges in the game
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [x.strip("\n") for x in lines]

    input_edges = [(x[: x.find("-")], x[x.find("-") + 1 :]) for x in lines]
    input_nodes = set(y[0] for y in input_edges) | set(y[1] for y in input_edges)

    input_edges = {
        x: [y[1] for y in input_edges if y[0] == x and y[1] != "start"]
        + [y[0] for y in input_edges if y[1] == x and y[0] != "start"]
        for x in input_nodes
    }

    return input_edges


def path_visited_lower_twice(path: List[str]) -> bool:
    """Test if a path visits a lower case node twice"""
    counts = {x: y for x, y in Counter(path).items() if x.islower() and x != "start"}
    return max(counts.values()) > 1


def find_paths(input_edges: Dict[str, str], visit_lower: bool = False) -> List[List[str]]:
    """
    Performs a recursive walk from the 'start' node to explore all possible branching steps that reach the 'end' node.

    If 'visit_single' then ONE lower case node can be visited twice.

    Records a list of paths from start -> end.
    """
    valid_paths = []
    incomplete_paths = [["start"]]
    while incomplete_paths:
        path = incomplete_paths.pop()
        possible_next_nodes = input_edges[path[-1]]

        for next_node in possible_next_nodes:
            if next_node == "end":
                valid_paths.append(path + [next_node])
            elif next_node[0].isupper() or next_node not in path:
                incomplete_paths.append(path + [next_node])
            elif next_node[0].islower() and visit_lower and not path_visited_lower_twice(path):
                incomplete_paths.append(path + [next_node])

    return valid_paths


def challenge_one(input_edges: Dict[str, str]) -> int:
    """Solves challenge one"""
    paths = find_paths(input_edges)
    return len(paths)


def challenge_two(input_edges: Dict[str, str]) -> int:
    """Solves challenge two"""
    paths = find_paths(input_edges, True)
    return len(paths)


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day12.txt"
    edges = setup_game(FILEPATH)

    # Challenge one
    challenge_one = challenge_one(input_edges=edges)
    print(f"Challenge one: {challenge_one}")

    # Challenge two
    challenge_two = challenge_two(input_edges=edges)
    print(f"Challenge two: {challenge_two}")
