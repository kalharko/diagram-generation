import argparse
from pathlib import Path

from diagram_generation import parse_class_descriptions_from_module
from diagram_generation.drawio.generate import convert_to_drawio
from diagram_generation.drawio.update import update_drawio
from diagram_generation.python.class_description import ClassDescription

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_path",
        help="Path to the folder to parse (required)",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output_path",
        help="Path to the output file (default diagram.drawio)",
        type=Path,
        default=Path.cwd() / "diagram.drawio",
    )
    parser.add_argument(
        "-f",
        "--force",
        help="Force overwrite of the output file, if omited, simply update the existing file (default False)",
        action="store_true",
    )

    args = parser.parse_args()

    # Check argument validity
    if not args.input_path.exists:
        raise ValueError(f"Path {args.input_path} is not a valid path.")
    if not args.input_path.is_dir:
        raise ValueError(f"Path {args.input_path} is not a directory.")
    if len(list(args.input_path.glob("__init__.py"))) != 1:
        raise ValueError(
            f"Path {args.input_path} does not contain a `__init__.py` file."
        )

    # Parse module informations
    class_descriptions: list[ClassDescription] = parse_class_descriptions_from_module(
        path=args.input_path
    )

    xml: str
    if args.force or not args.output_path.exists():
        # Generate new diagram
        xml = convert_to_drawio(descriptions=class_descriptions)

    else:
        # Update existing diagram
        with open(args.output_path, "r") as f:
            current_xml: str = f.read()
        xml = update_drawio(
            current_xml=current_xml, class_descriptions=class_descriptions
        )

    # Save diagram
    with open(args.output_path, "w") as f:
        f.write(xml)
    with open(args.output_path.with_suffix(".xml"), "w") as f:
        f.write(xml)
