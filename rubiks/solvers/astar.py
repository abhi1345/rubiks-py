from __future__ import annotations

from heapq import heappop, heappush
import time

from rubiks.cube import RubiksCube
from rubiks.heuristics import DEFAULT_HEURISTIC, Heuristic

from .common import SolveResult, should_prune_move


def solve_cube_astar(
    cube: RubiksCube,
    *,
    heuristic: Heuristic = DEFAULT_HEURISTIC,
    max_depth: int = 100,
) -> SolveResult:
    start = time.perf_counter()
    visited = set()
    explored = 0
    queue = [(heuristic(cube), cube.clone(), [])]

    while queue:
        _, cur_cube, moves_so_far = heappop(queue)

        state_key = cur_cube.state_tuple()
        if state_key in visited:
            continue
        visited.add(state_key)

        if cur_cube.is_solved():
            return SolveResult(True, moves_so_far, explored, time.perf_counter() - start)

        if len(moves_so_far) >= max_depth:
            continue

        for color in cur_cube.color_map:
            for turns in range(1, 4):
                move = (color, turns)
                if should_prune_move(moves_so_far, move):
                    continue

                next_cube = cur_cube.clone()
                next_cube.turn(color, turns)

                next_moves = moves_so_far + [move]

                if next_cube.state_tuple() in visited:
                    continue

                next_heuristic = len(next_moves) + heuristic(next_cube)
                heappush(queue, (next_heuristic, next_cube, next_moves))
                explored += 1

    return SolveResult(False, [], explored, time.perf_counter() - start)
