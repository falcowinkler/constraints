import copy

from algorithms.model import *
import algorithms.ac_3 as ac3


def consistent_with(constraint, assignment):
    constraint_fn = get_constraint_function(constraint)
    x_i, x_j = get_participating_variables(constraint)
    return constraint_fn(assignment[x_i], assignment[x_j]) \
        if x_i in assignment and x_j in assignment \
        else True


def is_consistent_with(constraints, assignment, variable, value):
    assignment = dict(assignment)
    assignment[variable] = value
    consistency_checks = [consistent_with(constraint, assignment) for constraint in constraints.items()]
    return False not in consistency_checks


def is_complete(assignment, variables):
    return assignment.keys() == variables.keys()


def select_unassigned_variable_mrv(variables, assignment):
    possible_choices = [var for var in variables.keys() if var not in assignment.keys()]
    return min(possible_choices, key=lambda var: len(variables[var]))


def count_conflicts(variable, value, constraints, variables):
    count = 0
    for neighbor in ac3.get_all_neighbors(constraints, variable):
        if value in variables[neighbor]:
            count += 1
    return count


def order_domain_values(variable, constraints, variables):
    return sorted(list(variables[variable]), key=lambda value: count_conflicts(variable,
                                                                               value,
                                                                               constraints,
                                                                               variables))


def get_unassigned_neighbors(constraints, assignment, variable):
    neighbors = ac3.get_all_neighbors(constraints, variable)
    return [(neighbor, variable)
            for neighbor in neighbors
            if neighbor not in assignment
            and (neighbor, variable) in dict(constraints)]


def forward_check(variables, variable, value, assignment, constraints):
    for neighbor in ac3.get_all_neighbors(constraints, variable):
        if neighbor not in assignment:
            if value in variables[neighbor]:
                variables[neighbor].remove(value)
                if len(variables[neighbor]) == 0:
                    return False


def backtrack(variables, constraints):
    ac3.ac3(constraints, variables, ac3.get_all_arcs(constraints))
    assignment = {k: next(iter(v)) for k, v in variables.items() if len(v) == 1}
    return _backtrack(variables, constraints, assignment)


def _backtrack(variables, constraints, assignment):
    if is_complete(assignment, variables):
        return assignment
    var = select_unassigned_variable_mrv(variables, assignment)
    for value in order_domain_values(var, constraints, variables):
        if is_consistent_with(constraints, assignment, var, value):
            assignment[var] = value
            local_vars = copy.deepcopy(variables)
            forward_check(local_vars, var, value, assignment, constraints)
            result = _backtrack(local_vars, constraints, assignment)
            if result is not False:
                return result
            del assignment[var]
    return False
