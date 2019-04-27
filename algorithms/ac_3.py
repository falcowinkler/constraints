from algorithms.model import *


def get_all_arcs(constraints):
    arcs = [get_participating_variables(constraint)
            for constraint in constraints
            if not is_unary(constraint)]
    return arcs


def all_false(boolean_list):
    return boolean_list == [False] * len(boolean_list)


def revised(constraints, variables, first, second):
    has_been_revised = False
    constraint = dict(constraints)[(first, second)]
    to_be_removed = set()
    for x_value in variables[first]:
        constraint_tests = [constraint(x_value, y_value) for y_value in variables[second]]
        if all_false(constraint_tests):
            to_be_removed.add(x_value)
            has_been_revised = True
    variables[first] -= to_be_removed
    return has_been_revised


def ac3(constraints, variables, queue):
    while queue:
        x_i, x_j = queue.pop()
        if revised(constraints, variables, x_i, x_j):
            if len(variables[x_i]) == 0:
                return False
            for neighbor in get_all_neighbors(constraints, x_i) - {x_j}:
                if (neighbor, x_i) in dict(constraints):
                    queue.append((neighbor, x_i))
    return True


def get_all_neighbors(constraints, variable):
    arcs = get_all_arcs(constraints)
    right_neighbor = [arc[1] for arc in arcs if arc[0] == variable]
    left_neighbor = [arc[0] for arc in arcs if arc[1] == variable]
    return set(left_neighbor + right_neighbor)
