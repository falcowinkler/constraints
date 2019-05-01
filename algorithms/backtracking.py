from algorithms.model import *
import algorithms.ac_3 as ac3
from collections import defaultdict


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


# Assumes you have only != constraints, for now
def count_conflicts(variable, value, neighbor_list, variables):
    count = 0
    for neighbor in ac3.get_all_neighbors(neighbor_list, variable):
        if value in variables[neighbor]:
            count += 1
    return count


def order_domain_values(variable, neighbor_list, variables):
    if len(variables[variable]) == 1:
        return variables[variable]
    return sorted(list(variables[variable]), key=lambda value: count_conflicts(variable,
                                                                               value,
                                                                               neighbor_list,
                                                                               variables))


def get_unassigned_neighbors(constraints, neighbors, assignment, variable):
    neighbors = ac3.get_all_neighbors(neighbors, variable)
    return [neighbor
            for neighbor in neighbors
            if neighbor not in assignment
            and (neighbor, variable) in dict(constraints)]


def forward_propagation(variables, variable, value, assignment, constraints, neighbors, pruned):
    for neighbor in get_unassigned_neighbors(constraints, neighbors, assignment, variable):
        to_be_removed = set()
        for neighbor_value in variables[neighbor]:
            if not constraints[(neighbor, variable)](neighbor_value, value):
                to_be_removed.add(value)
                pruned[variable].append((neighbor_value, neighbor))
        variables[neighbor] -= to_be_removed


def backtrack(variables, constraints):
    ac3.ac3(constraints, variables, ac3.get_all_arcs(constraints))
    assignment = {k: next(iter(v)) for k, v in variables.items() if len(v) == 1}
    pruned = defaultdict(list)
    neighbor_list = ac3.build_neighbors(constraints, variables)
    return _backtrack(variables, constraints, assignment, pruned, neighbor_list)


def _backtrack(variables, constraints, assignment, pruned, neighbor_list):
    if is_complete(assignment, variables):
        return assignment
    var = select_unassigned_variable_mrv(variables, assignment)
    for value in order_domain_values(var, neighbor_list, variables):
        if is_consistent_with(constraints, assignment, var, value):
            assignment[var] = value
            forward_propagation(variables, var, value, assignment, constraints, neighbor_list, pruned)
            if True:
                result = _backtrack(variables, constraints, assignment, pruned, neighbor_list)
                if result is not False:
                    return result
            for pruned_value, pruned_var in pruned[var]:
                variables[pruned_var].add(pruned_value)
            pruned[var] = list()
            del assignment[var]
    return False
