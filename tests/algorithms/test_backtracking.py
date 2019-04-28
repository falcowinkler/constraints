from unittest.mock import patch

import algorithms.backtracking as bt


def test_is_consistent_with():
    constraints = [(("A", "B"), lambda x, y: x >= y)]
    assignment = {"A": 2}
    assert bt.is_consistent_with(constraints, assignment, "B", 1)


def test_is_not_consistent_with():
    constraints = [(("A", "B"), lambda x, y: x >= y)]
    assignment = {"A": 2}
    assert not bt.is_consistent_with(constraints, assignment, "B", 3)


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


@patch("algorithms.ac_3.ac3", return_value=True)
def test_inference_mac(ac3_mock):
    constraints = [(("A", "B"), (lambda x, y: x > y))]
    variables = {"A": {3, 4, 5}, "B": {1}}
    assignment = {"B": 1}
    assert {"B": 1} == bt.inference_mac(constraints, variables, assignment, "B", 1)
    ac3_mock.assert_called_once_with(constraints, variables, [("A", "B")])


@patch("algorithms.ac_3.ac3", return_value=True)
def test_inference_mac(ac3_mock):
    constraints = [(("A", "B"), (lambda x, y: x > y))]
    variables = {"A": {3, 4, 5}, "B": {1, 2}}
    assignment = {"B": 1}
    assert bt.inference_mac(constraints, variables, assignment, "B", 1)
    ac3_mock.assert_called_once_with(constraints, {"A": {3, 4, 5}, "B": {1}}, [("A", "B")])
    assert {"A": {3, 4, 5}, "B": {1}} == variables


@patch("algorithms.ac_3.ac3", return_value=True)
def test_inference_mac_with_change_in_ac3_1(ac3_mock):
    constraints = [(("A", "B"), (lambda x, y: x > y)),
                   (("B", "C"), (lambda x, y: x >= y))]
    variables = {"A": {3, 4, 5}, "B": {1, 2}, "C": {2, 3}}
    assignment = {"B": 1}
    assert bt.inference_mac(constraints, variables, assignment, "B", 1)
    ac3_mock.assert_called_once_with(constraints, {"A": {3, 4, 5}, "B": {1}, "C": {2, 3}}, [("A", "B")])
    assert {"A": {3, 4, 5}, "B": {1}, "C": {2, 3}} == variables


def test_inference_mac_with_change_in_ac3():
    constraints = [(("A", "B"), (lambda x, y: x != y))]
    variables = {"A": {1, 2}, "B": {2}}
    assignment = {"B": 2}
    assert bt.inference_mac(constraints, variables, assignment, "B", 2)
    assert variables == {"A": {1}, "B": {2}}


def test_inference_mac_with_multiple_changes_in_ac3():
    constraints = [(("B", "A"), (lambda x, y: x < y)),
                   (("A", "B"), (lambda y, x: x < y)),
                   (("C", "B"), (lambda x, y: x != y)),
                   (("B", "C"), (lambda y, x: x != y))]
    variables = {"A": {1, 2, 3}, "B": {2, 3}, "C": {2, 3}}
    assignment = {"C": 3}
    assert {"A": 3, "B": 2, "C": 3} == bt.inference_mac(constraints, variables, assignment, "C", 3)


def test_failing_inference_mac_with_multiple_changes_in_ac3():
    constraints = [(("B", "A"), (lambda x, y: x < y)),
                   (("A", "B"), (lambda y, x: x < y)),
                   (("C", "B"), (lambda x, y: x != y)),
                   (("B", "C"), (lambda y, x: x != y))]
    variables = {"A": {1, 2, 3}, "B": {2, 3}, "C": {2, 3}}
    assignment = {"C": 2}
    assert not bt.inference_mac(constraints, variables, assignment, "C", 2)


def map_coloring_problem():
    countries = {"WA", "NT", "Q", "NSW", "V", "SA", "T"}
    variables = {country: {"red", "green", "blue"} for country in countries}
    neq = lambda x, y: x != y
    constraints = [(("SA", "WA"), neq),
                   (("SA", "NT"), neq),
                   (("SA", "Q"), neq),
                   (("SA", "NSW"), neq),
                   (("SA", "V"), neq),
                   (("WA", "NT"), neq),
                   (("NT", "Q"), neq),
                   (("Q", "NSW"), neq),
                   (("NSW", "V"), neq)]
    return variables, constraints


def test_backtracking_map_coloring():
    variables, constraints = map_coloring_problem()
    solution = bt.backtrack(variables, constraints)
    assert variables.keys() == solution.keys()
    for constraint in constraints:
        assert bt.consistent_with(constraint, solution)


# For now sort by conflicts with neighboring constraint (assuming we use alldif)
def test_least_constraining_value():
    variable = "A"
    constraints = [(("B", "A"), (lambda x, y: x != y)),
                   (("A", "B"), (lambda y, x: x != y)),
                   (("C", "A"), (lambda x, y: x != y)),
                   (("A", "C"), (lambda y, x: x != y))]
    variables = {"B": {1},
                 "A": {1, 2, 3},
                 "C": {1, 2}}
    assert [3, 2, 1] == bt.order_domain_values(variable, constraints, variables)


def test_least_constraining_value_map_coloring():
    variables, constraints = map_coloring_problem()
    variables["WA"] = {"green"}
    variables["NT"] = {"red"}
    variables["SA"] = {"blue"}
    assert "green" == bt.order_domain_values("Q", constraints, variables)[0]
