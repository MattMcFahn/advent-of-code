"""Solutions to day 7"""
from typing import List, Dict


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
        x: [y[1] for y in input_edges if y[0] == x] + [y[0] for y in input_edges if y[1] == x and y[0] != "start"]
        for x in input_nodes
    }

    return input_edges


def find_paths(input_edges: Dict[str, str]) -> List[List[str]]:
    """
    Performs a recursive walk from the 'start' node to explore all possible branching steps that reach the 'end' node.

    Lower case nodes can be visited only once.

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
            elif next_node != "start" and path[0] is None:
                new_path = path + [next_node]
                new_path[0] = next_node
                incomplete_paths.append(new_path)
    return valid_paths


def challenge_one(input_edges: Dict[str, str]) -> int:
    """Solves challenge one"""
    paths = find_paths(input_edges)
    return len(paths)


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day12.txt"
    edges = setup_game(FILEPATH)

    # Challenge one
    challenge_one = challenge_one(input_edges=edges)
    print(f"Challenge one: {challenge_one}")
