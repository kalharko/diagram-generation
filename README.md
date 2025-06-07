# diagram-generation
Static analysis of python code and generation of diagrams.

## Goals
- Parse a python module and it's sub module.
- Generate Entity Relationship Diagrams from parsed information.

## Data model
What information is parsed from a python module:
```
function
  name
  docstring
  decorators
  parameters and their type hints
  return values and their type hints

class
  name
  docstring
  responsabilities
  base classes
  members, their type hints and descriptions
  methods (same information as functions)
```

Responsabilities attribute is parsed from the docstring using the regex:
```regex
(?s)(Responsabilities:.*?)(?:\"\"\"|\n\n)
```

## Generated diagrams
The goal isn't to produce class diagrams, but an entity relationship diagram.