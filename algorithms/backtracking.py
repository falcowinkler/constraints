from algorithms.model import *
import algorithms.ac_3 as ac3
from collections import defaultdict


class ConstraintProblem:
    def __init__(self, variables, constraints):
        self.variables = variables
        self.constraints = constraints
        self.assignment = {k: next(iter(v)) for k, v in variables.items() if len(v) == 1}
        self.pruned = defaultdict(list)
        self.neighbor_list = ac3.build_neighbors(constraints, variables)


def consistent_with(constraint, assignment):
    constraint_fn = get_constraint_function(constraint)
    x_i, x_j = get_participating_variables(constraint)
    return constraint_fn(assignment[x_i], assignment[x_j]) \
        if x_i in assignment and x_j in assignment \
        else True


def is_consistent_with(cp, variable, value):
    for k, v in cp.assignment.items():
        left = (variable, k) in cp.constraints
        if not left and not (k, variable) in cp.constraints:
            continue
        constraint_fn = cp.constraints[(variable, k)] if left \
            else cp.constraints[(k, variable)]
        if k in cp.neighbor_list[variable] and not (constraint_fn(value, v) if left else constraint_fn(v, value)):
            return False
    return True


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


def get_unassigned_neighbors(cp, variable):
    neighbors = ac3.get_all_neighbors(cp.neighbor_list, variable)
    return [neighbor
            for neighbor in neighbors
            if neighbor not in cp.assignment
            and (neighbor, variable) in dict(cp.constraints)]


def forward_propagation(cp, variable, value):
    for neighbor in get_unassigned_neighbors(cp, variable):
        to_be_removed = set()
        for neighbor_value in cp.variables[neighbor]:
            if not cp.constraints[(neighbor, variable)](neighbor_value, value):
                to_be_removed.add(value)
                cp.pruned[variable].append((neighbor_value, neighbor))
        cp.variables[neighbor] -= to_be_removed


def backtrack(variables, constraints):
    ac3.ac3(constraints, variables, ac3.get_all_arcs(constraints))
    cp = ConstraintProblem(variables, constraints)
    return _backtrack(cp)


def _backtrack(cp):
    if is_complete(cp.assignment, cp.variables):
        return cp.assignment
    var = select_unassigned_variable_mrv(cp.variables, cp.assignment)
    for value in order_domain_values(var, cp.neighbor_list, cp.variables):
        if is_consistent_with(cp, var, value):
            cp.assignment[var] = value
            forward_propagation(cp, var, value)
            if True:
                result = _backtrack(cp)
                if result is not False:
                    return result
            for pruned_value, pruned_var in cp.pruned[var]:
                cp.variables[pruned_var].add(pruned_value)
            cp.pruned[var] = list()
            del cp.assignment[var]
    return False
