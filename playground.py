from RubiksCube import *

cube = RubiksCube()

cube.scramble()

cube.print_cube()

# print("\n\n### TURNING ### \n\n")

# for i in range(6):
#     cube.turn("green", 1)
#     cube.turn("red", 1)
#     cube.turn("green", 3)
#     cube.turn("red", 3)
#     print(cube.is_solved())

# cube.print_cube()