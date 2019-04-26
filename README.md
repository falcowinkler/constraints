### sudoku

constraint solving without libraries

### Notes

A constraint satisfaction problem consists of a set of variables X, domains D and constraints C.
X is a set of names, D a set of allowed values for each variable,
and a constraint is a pair `<scope, rel>` where scope is a tuple of variables that participate in the constraint,
and rel is a relation describing allowed values.

So i define a constraint as a tuple of a function, and a tuple of participating variables.
The variables and their domains shall be held in a dict, where the key is the variable name and the value is the domain, a generic list of any datatype.
