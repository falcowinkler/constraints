from itertools import combinations


def alldif(variables):
    c = list(combinations(variables, 2))
    return [(tuple(combi), lambda x, y: x != y) for combi in c]
