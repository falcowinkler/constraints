from algorithms.model import *


def consistent_with(constraint, assignment):
    constraint_fn = get_constraint_function(constraint)
    x_i, x_j = get_participating_variables(constraint)
    return constraint_fn(assignment[x_i], assignment[x_j]) \
        if x_i in assignment and x_j in assignment \
        else True


def is_consistent_with(constraints, assignment, variable, value):
    assignment = dict(assignment)
    assignment[variable] = value
    consistency_checks = [consistent_with(constraint, assignment) for constraint in constraints]
    return False not in consistency_checks


def is_complete(assignment, variables):
    return assignment.keys() == variables.keys()
