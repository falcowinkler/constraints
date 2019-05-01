def get_participating_variables(constraint):
    return constraint[0]


def get_constraint_function(constraint):
    return constraint[1]


def is_unary(constraint):
    return len(get_participating_variables(constraint)) == 1


def ensure_node_consistency(variables, constraints):
    for constraint in constraints.items():
        if is_unary(constraint):
            variable_to_restrict = get_participating_variables(constraint)[0]
            node_consistent = filter(get_constraint_function(constraint), variables[variable_to_restrict])
            variables[variable_to_restrict] = set(node_consistent)
    return variables


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

class ConstraintProblem:
    def __init__(self, variables, constraints):
        self.variables = variables
        self.constraints = constraints
        self.assignment = {k: next(iter(v)) for k, v in variables.items() if len(v) == 1}
        self.pruned = defaultdict(list)
        self.neighbor_list = build_neighbors(constraints, variables)


def consistent_with(constraint, assignment):
    constraint_fn = get_constraint_function(constraint)
    x_i, x_j = get_participating_variables(constraint)
    return constraint_fn(assignment[x_i], assignment[x_j]) \
        if x_i in assignment and x_j in assignment \
        else True


def is_consistent_with(cp, variable, value):
    for k, v in cp.assignment.items():
        if k in cp.neighbor_list[variable] and not cp.constraints[(variable, k)](value, v):
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
    for neighbor in get_all_neighbors(neighbor_list, variable):
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
    neighbors = get_all_neighbors(cp.neighbor_list, variable)
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
    ac3(constraints, variables, get_all_arcs(constraints))
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


from itertools import permutations


def alldif(variables):
    c = list(permutations(variables, 2))
    return {tuple(combi): lambda x, y: x != y for combi in c}


def sudoku(puzzle):
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
