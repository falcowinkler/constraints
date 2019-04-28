from algorithms.backtracking import *
from algorithms.node_consistency import *
from utility.constraint_factory import alldif

if __name__ == "__main__":
    puzzle = [[0, 0, 6, 1, 0, 0, 0, 0, 8],
              [0, 8, 0, 0, 9, 0, 0, 3, 0],
              [2, 0, 0, 0, 0, 5, 4, 0, 0],
              [4, 0, 0, 0, 0, 1, 8, 0, 0],
              [0, 3, 0, 0, 7, 0, 0, 4, 0],
              [0, 0, 7, 9, 0, 0, 0, 0, 3],
              [0, 0, 8, 4, 0, 0, 0, 0, 6],
              [0, 2, 0, 0, 5, 0, 0, 8, 0],
              [1, 0, 0, 0, 0, 2, 5, 0, 0]]

    print("Input sudoku puzzle: ")
    for row in puzzle:
        print(row)

    vars_x = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    vars_y = list(map(str, range(1, 10)))
    variables = dict()
    constraints = dict()
    for x in vars_x:
        for y in vars_y:
            variables[x + y] = set(range(1, 10))
    for x in vars_x:
        constraints.update(alldif([x + y for y in vars_y]))
    for y in vars_y:
        constraints.update(alldif([x + y for x in vars_x]))

    for base in range(1, 10, 3):
        for x in [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]:
            constraints.update(
                alldif([x[0] + str(base),
                        x[0] + str(base + 1),
                        x[0] + str(base + 2),
                        x[1] + str(base),
                        x[1] + str(base + 1),
                        x[1] + str(base + 2),
                        x[2] + str(base),
                        x[2] + str(base + 1),
                        x[2] + str(base + 2),
                        ]))

    # unary constraints
    unary = dict()
    for x in range(9):
        for y in range(9):
            if puzzle[y][x] != 0:
                unary[(vars_x[x] + vars_y[y],)] = lambda val, set_value=puzzle[y][x]: val == set_value
    variables = ensure_node_consistency(variables, unary)

    solution = backtrack(variables, constraints)
    if not solution:
        print("Found no solution")
    number_board_solution = [[None] * 9 for i in range(9)]
    for x_i, x in enumerate(vars_x):
        for y_i, y in enumerate(vars_y):
            number_board_solution[y_i][x_i] = solution[x + y]
    print("Solution")
    for row in number_board_solution:
        print(row)
