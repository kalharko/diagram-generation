from re import Match
import re
from typing import Iterator
from diagram_generation.python import DescriptionABC


class FunctionDescription(DescriptionABC):
    """Description of a python function.
    Responsabilities:
    - Describe a python function.
    """
    decorators: list[str]
    parameters: dict[str, str]  # {name: type hint}
    return_values: list[str]  # [type hint]

    def __init__(self, source: str) -> None:
        """
        Args:
            source (str): source string containing only the function.
        """
        self.source = source
        re_match: Match[str] | None
        re_iter_match: Iterator[Match[str]]

        # name
        re_match = re.search(
            pattern=r"def\s(\w+)\(",
            string=source
        )
        self.name: str = "" if re_match is None else re_match.group(1)

        # docstring
        re_match = re.search(
            pattern=r"(?s)\"\"\"(.*)\"\"\"",
            string=source,
            flags=re.MULTILINE,
        )
        self.docstring: str = "" if re_match is None else re_match.group(1)

        # decorators
        re_iter_match = re.finditer(
            pattern=r"^[\t ]*@(.+)$",
            string=source,
            flags=re.MULTILINE,
        )
        self.decorators: list[str] = []
        for re_match in re_iter_match:
            self.decorators.append(re_match.group(1))

        # parameters
        re_match = re.search(
            pattern=r"def \w+\((.*?)\)",
            string=source,
            flags=re.MULTILINE,
        )
        parameter_string: str = "" if re_match is None else re_match.group(1)
        print('...parameter string')
        print(parameter_string)
        re_iter_match = re.finditer(
            pattern=r"(?:^|,)[\t ]*(\w+)(?:[\t ]*:[\t ]*(?:(\w+\[.*?\])|(\w+))|())(?=(?:[^\]]*?,|[^\]]*?$))",
            string=parameter_string,
            flags=re.MULTILINE,
        )
        print('...re_iter_match')
        self.parameters: dict[str, str] = {}
        for re_match in re_iter_match:
            self.parameters[re_match.group(1)] = re_match.group(2) if re_match.group(2) is not None else re_match.group(3)

        # return values
        re_match = re.search(
            pattern=r"->\s?(.*):$",
            string=source,
            flags=re.MULTILINE,
        )
        return_string: str = "" if re_match is None else re_match.group(1)
        self.return_values: list[str]
        if return_string.startswith("tuple["):
            self.return_values = re.split(
                pattern=r"\s*,\s*",
                string=return_string[6:-1],
            )
        else:
            self.return_values = [return_string]
