### constraints

constraint solving without libraries. for practice.
implemented based on the book "Artificial Intelligence, a modern approach"
by Stuart Russell and Peter Norvig.

### run

to try a sudoku example, type ` pipenv run python sudoku_example/main.py `

### Notes

A constraint satisfaction problem consists of a set of variables X, domains D and constraints C.
X is a set of names, D a set of allowed values for each variable,
and a constraint is a pair `<scope, rel>` where scope is a tuple of variables that participate in the constraint,
and rel is a relation describing allowed values.

Here constraint is modelled as as a key, value pair (participating variables, function).
The variables and their domains should be held in a dict, where the key is the variable name and the value is the domain (as a set).

The algorithm uses the simplest version of backtracking, using forward propagation in every step.
It picks the most restrictive variable first for assignment, meaning the variable that has the smallest domain.

### todo

- make it faster! sudoku should be at least 10 times faster
- visualize assignment with graphviz https://www.python-course.eu/networkx.php
