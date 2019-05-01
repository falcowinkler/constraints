from collections import defaultdict


def get_all_arcs(constraints):
    return [k for k in constraints.keys() if not len(k) == 1]


def revised(constraints, variables, first, second):
    has_been_revised = False
    constraint = constraints[(first, second)]
    to_be_removed = set()
    for x_value in variables[first]:
        constraint_tests = [constraint(x_value, y_value) for y_value in variables[second]]
        if not any(constraint_tests):
            to_be_removed.add(x_value)
            has_been_revised = True
    variables[first] -= to_be_removed
    return has_been_revised


def build_neighbors(constraints, variables):
    neighbor_dict = defaultdict(set)
    for var in variables.keys():
        for constraint in constraints.keys():
            if constraint[0] == var:
                neighbor_dict[var].add(constraint[1])
            elif constraint[1] == var:
                neighbor_dict[var].add(constraint[0])
    return neighbor_dict


def ac3(constraints, variables, queue):
    neighbors = build_neighbors(constraints, variables)
    while queue:
        x_i, x_j = queue.pop()
        if revised(constraints, variables, x_i, x_j):
            if len(variables[x_i]) == 0:
                return False
            for neighbor in get_all_neighbors(neighbors, x_i) - {x_j}:
                if (x_i, neighbor) in constraints or (neighbor, x_i) in constraints:
                    queue.append((neighbor, x_i))
    return True


def get_all_neighbors(neighbor_dict, variable):
    return neighbor_dict[variable]
