"""Heuristic functions for Rubik's Cube solvers."""

import math
from typing import Protocol

from rubiks.constants import colors, opposite_color_map
from rubiks.cube import RubiksCube


class Heuristic(Protocol):
    def __call__(self, cube: RubiksCube) -> float: ...


def compute_number_of_misplaced_tiles(cube: RubiksCube) -> int:
    """Count stickers whose colors do not match the solved cube."""
    misplaced = 0
    for expected, side in enumerate(cube.state):
        for row in side:
            for tile in row:
                if tile != expected:
                    misplaced += 1
    return misplaced


def entropy_of_list(values):
    """Shannon entropy of a list interpreted as a probability distribution."""
    if not values:
        return 0.0

    total = len(values)
    entropy = 0.0
    for color in set(values):
        prob = values.count(color) / total
        entropy -= prob * math.log2(prob)
    return entropy


def entropy_of_matrix(matrix):
    return sum(entropy_of_list(row) for row in matrix)


def compute_entropy(cube: RubiksCube) -> float:
    """Sum of entropy per face; higher values means more disorder."""
    return sum(entropy_of_matrix(side) for side in cube.state)


def combined_entropy_misplaced(cube: RubiksCube) -> float:
    return compute_number_of_misplaced_tiles(cube) + compute_entropy(cube)

def pieces_distance_to_side(cube: RubiksCube):
    total_heuristic = 0

    for i, side in enumerate(cube.state):

        current_side = colors[i]

        for row in side:
            for piece in row:
                piece_color = colors[piece]
                total_heuristic += piece_distance_to_side(piece_color, current_side)

    return total_heuristic

def piece_distance_to_side(piece_color, current_side):
    if piece_color == current_side:
        return 0
    elif current_side == opposite_color_map[piece_color]:
        return 2
    else:
        return 1


DEFAULT_HEURISTIC: Heuristic = pieces_distance_to_side

__all__ = [
    "Heuristic",
    "DEFAULT_HEURISTIC",
    "compute_number_of_misplaced_tiles",
    "compute_entropy",
    "combined_entropy_misplaced",
    "pieces_distance_to_side",
]
