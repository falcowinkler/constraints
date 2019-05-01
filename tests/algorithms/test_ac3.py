import algorithms.ac_3 as ac3


def test_get_all_arcs_no_binary():
    constraints = {("SA",): (lambda x: x != "42"),
                   ("WA",): (lambda x: x > 123)}
    assert [] == ac3.get_all_arcs(constraints)


def test_get_all_arcs_one_binary():
    constraints = {("SA", "WA"): (lambda x, y: x != y)}
    assert [("SA", "WA")] == ac3.get_all_arcs(constraints)


def test_get_all_arcs_mixed():
    constraints = {("SA", "WA"): (lambda x: x != "wuff"),
                   ("WA",): (lambda x: x > 123),
                   ("DBC", "EFG"): (lambda x: x > 123)}
    assert [("SA", "WA"), ("DBC", "EFG")] == ac3.get_all_arcs(constraints)


def test_revise_not_revised():
    constraints = {("A", "B"): (lambda x, y: x != y)}
    variables = {"A": {1, 3, 5}, "B": {2, 4, 6}}
    assert not ac3.revised(constraints, variables, "A", "B")


def test_revised_1():
    constraints = {("A", "B"): (lambda x, y: x > y)}
    variables = {"A": {1, 2, 3}, "B": {2, 3, 4}}
    assert ac3.revised(constraints, variables, "A", "B")
    assert variables == {"A": {3}, "B": {2, 3, 4}}


def test_revised_2():
    constraints = {("A", "B"): (lambda x, y: x != y)}
    variables = {"A": {1, 2, 3}, "B": {2}}
    assert ac3.revised(constraints, variables, "A", "B")
    assert {"A": {1, 3}, "B": {2}} == variables


def test_ac3_no_changes():
    constraints = {("A", "B"): (lambda x, y: x > y)}
    variables = {"A": {3, 4, 5}, "B": {1}}
    assert ac3.ac3(constraints, variables, ac3.get_all_arcs(constraints))
    assert {"A": {3, 4, 5}, "B": {1}} == variables


def test_ac3_change_solvable():
    constraints = {("A", "B"): (lambda x, y: x != y)}
    variables = {"A": {1, 2, 3}, "B": {2}}
    assert ac3.ac3(constraints, variables, ac3.get_all_arcs(constraints))
    assert {"A": {1, 3}, "B": {2}} == variables


def test_ac3_change_solvable_multi_step():
    constraints = {("B", "A"): (lambda x, y: x < y),
                   ("A", "B"): (lambda y, x: x < y),
                   ("C", "B"): (lambda x, y: x != y),
                   ("B", "C"): (lambda y, x: x != y)}
    variables = {"A": {1, 2, 3}, "B": {2, 3}, "C": {2, 3}}
    assert ac3.ac3(constraints, variables, ac3.get_all_arcs(constraints))
    assert {"A": {3}, "B": {2}, "C": {3}} == variables


def test_ac3_unsolvable():
    constraints = {("A", "B"): (lambda x, y: x == y)}
    variables = {"A": {1, 2, 3}, "B": {42}}
    assert not ac3.ac3(constraints, variables, ac3.get_all_arcs(constraints))


def test_get_neighbors():
    assert {"WA", "V"} == ac3.get_all_neighbors({"SA": {"WA", "V"}}, "SA")
