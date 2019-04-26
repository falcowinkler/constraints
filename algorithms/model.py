def get_participating_variables(constraint):
    return constraint[0]


def get_constraint_function(constraint):
    return constraint[1]


def is_unary(constraint):
    return len(get_participating_variables(constraint)) == 1
