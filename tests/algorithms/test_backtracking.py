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
