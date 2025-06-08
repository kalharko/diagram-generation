import argparse
import re
from pathlib import Path
from re import Match
from typing import Iterator

from diagram_generation import parse_class_descriptions_from_module
from diagram_generation.python.class_description import ClassDescription

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        help="path to the folder to treat",
        type=Path,
    )
    args = parser.parse_args()

    # Check argument validity
    if not args.path.exists:
        raise ValueError(f"Path {args.path} is not a valid path.")
    if not args.path.is_dir:
        raise ValueError(f"Path {args.path} is not a directory.")
    if len(list(args.path.glob("__init__.py"))) != 1:
        raise ValueError(f"Path {args.path} does not contain a `__init__.py` file.")

    # Parse module informations
    class_descriptions: list[ClassDescription] = parse_class_descriptions_from_module(path=args.path)

    # Render class descriptions
    for class_description in class_descriptions:
        print(class_description)
