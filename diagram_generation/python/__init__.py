import re
from abc import ABC, abstractmethod
from typing import Any


class DescriptionABC(ABC):
    """Abstract base class for object descriptions."""

    source: str  # source string from which the description is extracted
    name: str  # name of the described object
    docstring: str  # docstring of the described object

    @abstractmethod
    def __init__(self, source: str) -> None:
        """
        Args:
            source (str): source string containing only the described object.
        """
        raise NotImplementedError

    @property
    def responsability(self) -> str:
        """Parses the responsability paragraph in the function's docstring.
        Returns:
            str: The responsability paragraph, might be an empty string.
        """

        rematch = re.search(
            pattern=r"(?s)(Responsabilities:.*?)(?:\Z|\n\n)",
            string=self.docstring,
            flags=re.MULTILINE,
        )
        return "" if rematch is None else rematch.group(1)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def __str__(self) -> str:
        out = f"{self.name}:\n"
        for key, value in self.__dict__.items():
            if isinstance(value, list) and len(value) > 0:
                out += f"{key}:\n"
                val: Any
                for val in value:
                    out += f"- {val}\n"
            else:
                out += f"{key}: {value}\n"

        return out
