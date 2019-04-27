from algorithms.model import *
import algorithms.ac_3 as ac3
import random

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


def select_unassigned_variable_mrv(variables, assignment):
    possible_choices = [var for var in variables.keys() if var not in assignment.keys()]
    return min(possible_choices, key=lambda var: len(variables[var]))


def order_domain_values(variable, constraints, variables, assignment):
    return sorted(variables[variable])  # TODO: implement least-constraining value


def get_unassigned_neighbors(constraints, assignment, variable):
    neighbors = ac3.get_all_neighbors(constraints, variable)
    return [(neighbor, variable)
            for neighbor in neighbors
            if neighbor not in assignment
            and (neighbor, variable) in dict(constraints)]


def inference(constraints, variables, assignment, variable, value):
    variables_copy = dict(variables)
    for k, v in assignment.items():
        variables_copy[k] = {v}
    variables_copy[variable] = {value}
    if ac3.ac3(constraints, variables_copy, get_unassigned_neighbors(constraints, assignment, variable)):
        return {var: next(iter(inferred)) for var, inferred in variables_copy.items() if len(inferred) == 1}
    else:
        return False


def backtrack(variables, constraints):
    return _backtrack(variables, constraints, {})


def _backtrack(variables, constraints, assignment):
    if is_complete(assignment, variables):
        return assignment
    var = select_unassigned_variable_mrv(variables, assignment)
    for value in order_domain_values(var, constraints, variables, assignment):
        inferences = dict()
        if is_consistent_with(constraints, assignment, var, value):
            assignment[var] = value
            inferred = inference(constraints, variables, assignment, var, value)
            if inferred is not False:
                assignment.update(inferred)
                result = _backtrack(variables, constraints, assignment)
                if result is not False:
                    return result
        if var in assignment:
            del assignment[var]
        for v in inferences.keys():
            if v in assignment:
                del assignment[v]
    return False
