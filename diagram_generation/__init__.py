import re
from pathlib import Path
from re import Match
from typing import Iterator

from diagram_generation.python.class_description import ClassDescription


def parse_class_descriptions_from_module(path: Path) -> list[ClassDescription]:
    """Parses a python module and returns a list of ClassDescription objects.

    Args:
        path (Path): Path to the python module.

    Returns:
        list[ClassDescription]: List of ClassDescription objects.
    """

    class_descriptions: list[ClassDescription] = []

    # Walk all python files at the given path and its subfolders
    for path in path.glob("**/*.py"):
        # Read the file
        with path.open("r") as f:
            source = f.read()

        # Get the classes sources
        re_iter_match: Iterator[Match[str]] | None = re.finditer(
            pattern=r"(?s)^(class.*?)(?=(?:^\w|\Z))",
            string=source,
            flags=re.MULTILINE,
        )
        for class_source in re_iter_match:
            class_descriptions.append(ClassDescription(class_source.group(1)))

    return class_descriptions
