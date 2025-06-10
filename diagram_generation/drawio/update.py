
import re
from re import Match
from typing import Iterator
from diagram_generation.drawio.generate import class_full_drawio_table, get_members_value_height, get_methods_value_height, get_responsability_value_height
from diagram_generation.python.class_description import ClassDescription


def update_drawio(current_xml: str, class_descriptions: list[ClassDescription]) -> str:
    """Parses the current xml and replace it's values with the new ones.
    Args:
        current_xml (str): Current xml string.
        class_descriptions (list[ClassDescription]): List of ClassDescription objects.

    Returns:
        str: Updated xml string.
    """

    # Store the classes to be added to the current xml
    classes_to_be_added: list[ClassDescription] = []

    for description in class_descriptions:
        responsability_text, responsability_height = get_responsability_value_height(description)
        members_text, members_height = get_members_value_height(description)
        methods_text, methods_height = get_methods_value_height(description)

        # Parse class id in current_xml
        re_match: Match[str] | None
        re_match = re.search(
            pattern=f"<mxCell id=\"(.*)\" value=\"{description.name}\"",
            string=current_xml,
            flags=re.MULTILINE,
        )
        if re_match is None:
            classes_to_be_added.append(description)
            continue

        id: int = int(re_match.group(1))

        # Replace class values
        current_xml = re.sub(
            pattern=f"(<mxCell id=\"{id + 1}\" value=\").*?(\")",
            repl=f"\\1{responsability_text}\\2",
            string=current_xml,
            flags=re.MULTILINE,
        )
        current_xml = re.sub(
            pattern=f"(<mxCell id=\"{id + 1}\"(?:.|\n)*?mxGeometry.*?height=\").*?(\")",
            repl=f"\\1{responsability_height}\\2",
            string=current_xml,
            flags=re.MULTILINE,
        )
        current_xml = re.sub(
            pattern=f"(<mxCell id=\"{id + 2}\" value=\").*?(\")",
            repl=f"\\1{members_text}\\2",
            string=current_xml,
            flags=re.MULTILINE,
        )
        current_xml = re.sub(
            pattern=f"(<mxCell id=\"{id + 2}\"(?:.|\n)*?mxGeometry.*?height=\").*?(\")",
            repl=f"\\1{members_height}\\2",
            string=current_xml,
            flags=re.MULTILINE,
        )
        current_xml = re.sub(
            pattern=f"(<mxCell id=\"{id + 3}\" value=\").*?(\")",
            repl=f"\\1{methods_text}\\2",
            string=current_xml,
            flags=re.MULTILINE,
        )
        current_xml = re.sub(
            pattern=f"(<mxCell id=\"{id + 3}\"(?:.|\n)*?mxGeometry.*?height=\").*?(\")",
            repl=f"\\1{methods_height}\\2",
            string=current_xml,
            flags=re.MULTILINE,
        )

    # Add new classes
    max_id: int = _get_max_id_in_drawio(current_xml)
    to_be_added_xml: str = ""
    for i, description in enumerate(classes_to_be_added):
        to_be_added_xml += class_full_drawio_table(description, max_id + i * 4 + 1)

    current_xml = re.sub(
        pattern=r"(\n)(?=[\t ]*</root>)",
        repl='\n' + to_be_added_xml + '\n',
        string=current_xml,
        flags=re.MULTILINE,
    )

    return current_xml


def _get_max_id_in_drawio(xml: str) -> int:
    re_iter_match: Iterator[Match[str]] | None = re.finditer(
        pattern=r"<mxCell id=\"(\d+)\"",
        string=xml,
        flags=re.MULTILINE,
    )

    return max(
        int(re_match.group(1))
        for re_match in re_iter_match
    )
