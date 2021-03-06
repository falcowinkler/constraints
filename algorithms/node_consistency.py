from algorithms.model import *


def ensure_node_consistency(variables, constraints):
    for constraint in constraints.items():
        if is_unary(constraint):
            variable_to_restrict = get_participating_variables(constraint)[0]
            node_consistent = filter(get_constraint_function(constraint), variables[variable_to_restrict])
            variables[variable_to_restrict] = set(node_consistent)
    return variables
