import algorithms.ac_3 as ac3


def test_get_all_arcs_no_binary():
    constraints = [(("SA",), (lambda x: x != "42")),
                   (("WA",), (lambda x: x > 123))]
    assert [] == ac3.get_all_arcs(constraints)


def test_get_all_arcs_one_binary():
    constraints = [(("SA", "WA"), (lambda x, y: x != y))]
    assert [("SA", "WA")] == ac3.get_all_arcs(constraints)


def test_get_all_arcs_mixed():
    constraints = [(("SA", "WA"), (lambda x: x != "wuff")),
                   (("WA",), (lambda x: x > 123)),
                   (("DBC", "EFG"), (lambda x: x > 123))]
    assert [("SA", "WA"), ("DBC", "EFG")] == ac3.get_all_arcs(constraints)


def test_revise_not_revised():
    constraints = [(("A", "B"), (lambda x, y: x != y))]
    variables = {"A": {1, 3, 5}, "B": {2, 4, 6}}
    assert not ac3.revised(constraints, variables, "A", "B")


def test_revised_1():
    constraints = [(("A", "B"), (lambda x, y: x > y))]
    variables = {"A": {1, 2, 3}, "B": {2, 3, 4}}
    assert ac3.revised(constraints, variables, "A", "B")
    assert variables == {"A": {3}, "B": {2, 3, 4}}


def test_revised_2():
    constraints = [(("A", "B"), (lambda x, y: x != y))]
    variables = {"A": {1, 2, 3}, "B": {2}}
    assert ac3.revised(constraints, variables, "A", "B")
    assert variables == {"A": {1, 3}, "B": {2}}
