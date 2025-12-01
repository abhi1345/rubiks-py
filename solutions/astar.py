import copy
import time
from heapq import heappush, heappop

def compute_number_of_misplaced_tiles_heuristic(cube):
    
    output = 0

    for expected, side in enumerate(cube.state):
        for row in side:
            for tile in row:
                if tile != expected:
                    output += 1

    return output

def solve_cube_astar(cube):
    visited = set()

    starting_heuristic = compute_number_of_misplaced_tiles_heuristic(cube)

    bfs_queue = [(starting_heuristic, cube, [])]

    while bfs_queue:

        cur_heuristic, cur_cube, moves_so_far = heappop(bfs_queue)

        if cur_cube.state_tuple() in visited:
            continue

        visited.add(cur_cube.state_tuple())

        if cur_cube.is_solved():
            return True, moves_so_far

        if len(moves_so_far) > 100:
            return False, moves_so_far

        for color in cur_cube.color_map:
            for n in range(1, 4):
                new_cube = copy.deepcopy(cur_cube)
                new_cube.turn(color, n)

                new_moves_so_far = moves_so_far + [(color, n)]

                if new_cube.is_solved():
                    return True, new_moves_so_far
                if new_cube.state_tuple() in visited:
                    continue

                new_heuristic = len(new_moves_so_far) + compute_number_of_misplaced_tiles_heuristic(new_cube)

                heappush(bfs_queue, (new_heuristic, new_cube, new_moves_so_far))
    
    return False, ["Coudn't Solve"]