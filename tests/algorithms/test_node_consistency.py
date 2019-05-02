import os
import logging as log

import algorithms.node_consistency as nc


def test_node_consistency_no_unary_constraints():
    variables = {
        "SA": {"red", "green", "blue"},
        "WA": {"red", "green", "blue"}
    }
    constraints = {("SA", "WA"): (lambda x, y: x != y)}
    node_consistent_variables = nc.ensure_node_consistency(variables, constraints)
    assert variables == node_consistent_variables
    assert {"A", "B"} == {"B", "A"}


def test_node_consistency():
    variables = {
        "SA": {"red", "green", "blue"},
        "WA": {"red", "green", "blue"}
    }
    constraints = {("SA",): (lambda x: x != "green")}
    node_consistent_variables = nc.ensure_node_consistency(variables, constraints)
    assert node_consistent_variables == {
        "SA": {"red", "blue"},
        "WA": {"red", "green", "blue"}
    }
