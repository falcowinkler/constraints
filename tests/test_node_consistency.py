import os
import logging as log

log.error(os.getcwd())
print(os.getcwd())
import algorithms.node_consistency as nc


def test_node_consistency_no_unary_constraints():
    variables = {
        "SA": ["red", "green", "blue"],
        "WA": ["red", "green", "blue"]
    }
    constraints = [((lambda x, y: x != y), ("SA", "WA"))]
    node_consistent_variables = nc.ensure_node_consistency(variables, constraints)
    assert variables == node_consistent_variables


def test_node_consistency():
    variables = {
        "SA": ["red", "green", "blue"],
        "WA": ["red", "green", "blue"]
    }
    constraints = [((lambda x: x != "green"), ("SA",))]
    node_consistent_variables = nc.ensure_node_consistency(variables, constraints)
    assert node_consistent_variables == {
        "SA": ["red", "blue"],
        "WA": ["red", "green", "blue"]
    }
