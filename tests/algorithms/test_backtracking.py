from unittest.mock import patch
from collections import defaultdict
import algorithms.backtracking as bt
from algorithms.ac_3 import build_neighbors


def test_is_consistent_with():
    constraints = {("B", "A"): lambda x, y: x <= y}
    assert bt.is_consistent_with(bt.ConstraintProblem({"A": {2}}, constraints), "B", 1)


def test_is_not_consistent_with():
    constraints = {("B", "A"): lambda x, y: x <= y}
    cp = bt.ConstraintProblem({"A": {2}, "B": {1, 2, 3}}, constraints)
    assert not bt.is_consistent_with(cp, "B", 3)


def test_is_complete():
    variables = {"A": [1, 2, 3], "B": ["wiff", "wuff", "waff"], "C": ["foo", "bar", "baz"]}
    assignment = {"A": 1, "B": "wiff", "C": "foo"}
    assert bt.is_complete(assignment, variables)


def test_is_complete_incomplete():
    variables = {"A": [1, 2, 3], "B": ["wiff", "wuff", "waff"], "C": ["foo", "bar", "baz"]}
    assignment = {"A": 1}
    assert not bt.is_complete(assignment, variables)


def test_select_unassigned_variable():
    variables = {"A": [1, 2, 3], "B": ["wiff", "wuff"], "C": ["foo", "bar", "baz", "clazz"]}
    assignment = {}
    assert "B" == bt.select_unassigned_variable_mrv(variables, assignment)


def test_select_unassigned_variable_with_assignment():
    variables = {"A": [1, 2, 3], "B": ["wiff", "wuff"], "C": ["foo", "bar", "baz", "clazz"]}
    assignment = {"B": "wuff"}
    assert "A" == bt.select_unassigned_variable_mrv(variables, assignment)


def map_coloring_problem():
    countries = {"WA", "NT", "Q", "NSW", "V", "SA", "T"}
    variables = {country: {"red", "green", "blue"} for country in countries}
    neq = lambda x, y: x != y
    constraints = {("SA", "WA"): neq,
                   ("SA", "NT"): neq,
                   ("SA", "Q"): neq,
                   ("Q", "SA"): neq,
                   ("SA", "NSW"): neq,
                   ("SA", "V"): neq,
                   ("WA", "NT"): neq,
                   ("NT", "Q"): neq,
                   ("Q", "NSW"): neq,
                   ("NSW", "V"): neq}
    return variables, constraints


def test_backtracking_map_coloring():
    variables, constraints = map_coloring_problem()
    solution = bt.backtrack(variables, constraints)
    assert variables.keys() == solution.keys()
    for constraint in constraints.items():
        assert bt.consistent_with(constraint, solution)


# For now sort by conflicts with neighboring constraint (assuming we use alldif)
def test_least_constraining_value():
    variable = "A"
    constraints = {("B", "A"): (lambda x, y: x != y),
                   ("A", "B"): (lambda y, x: x != y),
                   ("C", "A"): (lambda x, y: x != y),
                   ("A", "C"): (lambda y, x: x != y)}
    variables = {"B": {1},
                 "A": {1, 2, 3},
                 "C": {1, 2}}
    assert [3, 2, 1] == bt.order_domain_values(variable, build_neighbors(constraints, variables), variables)


def test_least_constraining_value_map_coloring():
    variables, constraints = map_coloring_problem()
    variables["WA"] = {"green"}
    variables["NT"] = {"red"}
    variables["SA"] = {"blue"}
    assert "blue" != bt.order_domain_values("Q", build_neighbors(constraints, variables), variables)[0]


def test_forward_check():
    variables, constraints = map_coloring_problem()
    variables["WA"] = {"green"}
    variables["NT"] = {"red"}
    cp = bt.ConstraintProblem(variables, constraints)
    bt.forward_propagation(cp, "Q", "blue")
    assert variables["SA"] == {"green", "red"}
    # remember that forward check from Q pruned the blue choice from SA, so we can revert the change later
    # and avoid copys of our variable domains
    assert cp.pruned["Q"] == [("blue", "SA")]
