import copy
import time

def solve_cube_bfs(cube):
    visited = set()
    bfs_queue = [(cube, [])]

    while bfs_queue:

        cur_cube, moves_so_far = bfs_queue.pop(0)

        if cur_cube.state_tuple() in visited:
            continue

        visited.add(cur_cube.state_tuple())

        if cur_cube.is_solved():
            return True, moves_so_far

        if len(moves_so_far) > 100:
            return False, moves_so_far

        for color in cur_cube.color_map:
            for n in range(1, 4):

                if len(moves_so_far) > 0:
                    if (color, n) == moves_so_far[-1]:
                        continue
                    elif (color, 4-n) == moves_so_far[-1]:
                        continue

                new_cube = copy.deepcopy(cur_cube)
                new_cube.turn(color, n)

                new_moves_so_far = moves_so_far + [(color, n)]

                if new_cube.is_solved():
                    return True, new_moves_so_far
                if new_cube.state_tuple() in visited:
                    continue

                bfs_queue.append((new_cube, new_moves_so_far))
    
    return False, ["Coudn't Solve"]