import utility.constraint_factory as cf
from algorithms.model import *
from itertools import combinations


def test_alldif():
    variables = ["A", "B", "C"]
    alldif = cf.alldif(variables)
    constraint_variables = {get_participating_variables(constraint) for constraint in alldif}
    assert constraint_variables == set(combinations(variables, 2))
