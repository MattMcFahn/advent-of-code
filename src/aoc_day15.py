"""Solutions to day 15 - dijkstra's algorithm"""
from itertools import product
from typing import Dict
from queue import PriorityQueue
from datetime import datetime

import pandas as pd

# pylint: disable=unnecessary-comprehension,too-many-locals


class Graph:
    """Graph class, helpfully initialised from a weight matrix"""

    def __init__(self, weights: pd.DataFrame):
        self.number_of_vertices = weights.shape[0] * weights.shape[1]
        self.vertices = [x for x in product(range(0, weights.shape[0]), range(0, weights.shape[1]))]
        self.edges = {x: {} for x in self.vertices}
        self.setup_edges(weights)
        self.visited = []

    def add_edge(self, u, v, weight):
        """Helper to add a single edge to this Graph structure.
        Weight to move:
            > From: U
            > To: V
        """
        self.edges[u][v] = weight

    def setup_edges(self, weights: pd.DataFrame):
        """Initialise all edges and weights. The (i, j)th position in the dataframe has vertex label (i, j)"""
        for row_index, column in weights.iteritems():
            for col_index, weight in column.iteritems():
                surrounding_points = [
                    (row_index - 1, col_index),
                    (row_index + 1, col_index),
                    (row_index, col_index - 1),
                    (row_index, col_index + 1),
                ]
                surrounding_points = [
                    x
                    for x in surrounding_points
                    if x[0] not in (-1, weights.shape[0]) and x[1] not in (-1, weights.shape[1])
                ]
                for point in surrounding_points:
                    self.add_edge(point, (row_index, col_index), int(weight))


def setup_game(filepath: str) -> Graph:
    """
    From the input filepath, reads the input sequence, and rules
    """
    with open(filepath) as file:
        lines = file.readlines()
    lines = [list(x.strip("\n")) for x in lines]

    weights = pd.DataFrame(lines)

    input_graph = Graph(weights)

    return input_graph


def setup_second_game(filepath):
    """Helper to set up the graph for the second game"""
    with open(filepath) as file:
        lines = file.readlines()
    lines = [list(x.strip("\n")) for x in lines]

    weights = pd.DataFrame(lines)
    for column in weights.columns:
        weights[column] = weights[column].astype(int)

    weights_plus_one = weights.copy() + 1
    weights_plus_two = weights.copy() + 2
    weights_plus_three = weights.copy() + 3
    weights_plus_four = weights.copy() + 4

    for frame in [weights_plus_one, weights_plus_two, weights_plus_three, weights_plus_four]:
        for column in frame.columns:
            frame[column] = (frame[column] + -1).mod(9) + 1

    new_frame = pd.concat(
        [weights, weights_plus_one, weights_plus_two, weights_plus_three, weights_plus_four], ignore_index=True
    )

    new_frame_plus_one = new_frame.copy() + 1
    new_frame_plus_two = new_frame_plus_one.copy() + 1
    new_frame_plus_three = new_frame_plus_two.copy() + 1
    new_frame_plus_four = new_frame_plus_three.copy() + 1

    for frame in [new_frame_plus_one, new_frame_plus_two, new_frame_plus_three, new_frame_plus_four]:
        for column in frame.columns:
            frame[column] = (frame[column] + -1).mod(9) + 1

    final_frame = pd.concat(
        [new_frame, new_frame_plus_one, new_frame_plus_two, new_frame_plus_three, new_frame_plus_four],
        axis=1,
        ignore_index=True,
    )

    input_graph = Graph(final_frame)
    return input_graph


def create_costs(graph: Graph, start_vertex: tuple) -> Dict[tuple, int]:
    """Implements dijkstra's"""
    costs = {vertex: float("inf") for vertex in graph.vertices}
    costs[start_vertex] = 0

    queue = PriorityQueue()
    queue.put((0, start_vertex))
    print(f"There are {graph.number_of_vertices} vertices to visit")
    while not queue.empty():
        number_visited = len(graph.visited)
        if number_visited % 20000 == 0:
            print(f"{datetime.now()} Number visited: {len(graph.visited)}")
        current_cost, vertex = queue.get()
        graph.visited.append(vertex)

        for next_vertex, cost in graph.edges[vertex].items():
            if next_vertex not in graph.visited:
                old_cost = costs[next_vertex]
                new_cost = current_cost + cost
                if new_cost < old_cost:
                    queue.put((new_cost, next_vertex))
                    costs[next_vertex] = new_cost
    return costs


def calculate(graph: Graph) -> int:
    """Solves challenge one and two, effectively just a wrapper around dijkstra's"""
    start_vertex = (0, 0)
    costs = create_costs(graph=graph, start_vertex=start_vertex)
    return costs[graph.vertices[-1]]


if __name__ == "__main__":
    FILEPATH = r"./resources/aoc-day15.txt"
    print("Setting up graph for challenge one... ")
    challenge_one_graph = setup_game(filepath=FILEPATH)
    print("Setting up graph for challenge one... DONE")

    # Challenge one
    print("Starting challenge one... ")
    challenge_one = calculate(graph=challenge_one_graph)
    print(f"Challenge one: {challenge_one}")

    # Challenge two
    print("Setting up graph for challenge two... ")
    challenge_two_graph = setup_second_game(filepath=FILEPATH)
    print("Setting up graph for challenge two... DONE")
    print("Starting challenge two... ")
    challenge_two = calculate(graph=challenge_two_graph)
    print(f"Challenge two: {challenge_two}")
