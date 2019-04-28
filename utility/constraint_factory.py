from itertools import permutations


def alldif(variables):
    c = list(permutations(variables, 2))
    return [(tuple(combi), lambda x, y: x != y) for combi in c]
