### constraints

constraint solving without libraries. for practice.
implemented based on the book "Artificial Intelligence, a modern approach"
by Stuart Russell and Peter Norvig.

It's still pretty slow because `order_domain_values` is not yet sophisticated.

### run

to try a sudoku example, type ` pipenv run python sudoku_example/main.py `

### Notes

A constraint satisfaction problem consists of a set of variables X, domains D and constraints C.
X is a set of names, D a set of allowed values for each variable,
and a constraint is a pair `<scope, rel>` where scope is a tuple of variables that participate in the constraint,
and rel is a relation describing allowed values.

So i define a constraint as a tuple of a function, and a tuple of participating variables.
The variables and their domains should be held in a dict, where the key is the variable name and the value is the domain, a generic list of any datatype.
