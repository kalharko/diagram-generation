import re
from re import Match
from typing import Iterator

from diagram_generation.python import DescriptionABC
from diagram_generation.python.function_description import FunctionDescription


class ClassDescription(DescriptionABC):
    """Description of a python class.
    Responsabilities:
    - Describe a python class.
    """

    base_classes: list[str]
    members: dict[str, tuple[str, str]]  # {name: (type hint, description)}
    methods: list[FunctionDescription]

    def __init__(self, source: str) -> None:
        """
        Args:
            source (str): source string containing only the class.
        """
        self.source = source
        re_match: Match[str] | None
        re_iter_match: Iterator[Match[str]]

        # name
        re_match = re.search(pattern=r"class\s(\w+)\(", string=source)
        self.name = "" if re_match is None else re_match.group(1)

        # docstring
        re_match = re.search(
            pattern=r"(?s)\"\"\"(.*?)\"\"\"",
            string=source,
            flags=re.MULTILINE,
        )
        self.docstring = "" if re_match is None else re_match.group(1)

        # base classes
        re_match = re.search(
            pattern=r"^class\s\w+\((.*)\):\n",
            string=source,
            flags=re.MULTILINE,
        )
        base_class_string: str = "" if re_match is None else re_match.group(1)
        self.base_classes: list[str] = re.split(
            pattern=r"\s*,\s*", string=base_class_string
        )

        # members
        re_match = re.search(
            pattern=r"class .*\n[\t ]*\"\"\"(?:.|\n)*?\"\"\"\n(([\t ]*).*(?:\n\2.*)*?)(?:\n\n|@|def)",
            string=source,
            flags=re.MULTILINE,
        )
        members_string: str = "" if re_match is None else re_match.group(1)
        re_iter_match = re.finditer(
            pattern=r"^[\t ]+(\w+)[\t ]*:[\t ]*(.+?)(?:[\t ]+#[\t ]+(.*)|())$",
            string=members_string,
            flags=re.MULTILINE,
        )
        self.members: dict[str, tuple[str, str]] = {}
        for re_match in re_iter_match:
            self.members[re_match.group(1)] = (re_match.group(2), re_match.group(3))

        # methods  # limitation: break on functions that have docstring at indentation 0.
        re_iter_match = re.finditer(
            pattern=r"^((?:[\t ]*@.*\n)*[\t ]*def.*:\n([\t ]*).*(?:\n+\2.*)*)",
            string=source,
            flags=re.MULTILINE,
        )
        self.methods: list[FunctionDescription] = []
        for re_match in re_iter_match:
            self.methods.append(FunctionDescription(re_match.group(1)))

    @property
    def method_names(self) -> list[str]:
        return [method.name for method in self.methods]
