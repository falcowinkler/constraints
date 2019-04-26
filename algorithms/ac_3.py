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
