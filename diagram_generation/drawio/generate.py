from diagram_generation.python.class_description import ClassDescription


def convert_to_drawio(descriptions: list[ClassDescription]) -> str:
    out: str = """
<mxfile host="65bd71144e">
    <diagram id="k2kCJi-R33WXwNhiQUoG" name="Page-1">
        <mxGraphModel dx="910" dy="409" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
"""

    for i, description in enumerate(descriptions):
        out += class_full_drawio_table(description, i * 4 + 2)

    out += """
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
    """
    return out


def _class_short_drawio_table(description: ClassDescription, id: int) -> str:
    """Builds the XML representation of a class.
    Returns:
        str: The XML representation of the class.
    """

    core_text = description.responsability.replace("\n", "&lt;br&gt;")

    return f"""<mxCell id="{id}" value="{description.name}" style="swimlane;whiteSpace=wrap;html=1;" vertex="1" parent="1">
    <mxGeometry x="40" y="120" width="200" height="200" as="geometry"/>
</mxCell>
<mxCell id="{id + 1}" value="{core_text}" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;" vertex="1" parent="{id}">
    <mxGeometry y="30" width="200" height="170" as="geometry"/>
</mxCell>"""


def class_full_drawio_table(description: ClassDescription, id: int) -> str:
    """Builds the full XML representation of a class.
    Returns:
        str: The XML representation of the class.
    """
    responsability_text, responsability_height = get_responsability_value_height(
        description
    )
    members_text, members_height = get_members_value_height(description)
    methods_text, methods_height = get_methods_value_height(description)

    return f"""<mxCell id="{id}" value="{description.name}" style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
        <mxGeometry x="60" y="180" width="220" height="110" as="geometry"/>
    </mxCell>
    <mxCell id="{id + 1}" value="{responsability_text}" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;" vertex="1" parent="{id}">
        <mxGeometry y="30" width="220" height="{responsability_height}" as="geometry"/>
    </mxCell>
    <mxCell id="{id + 2}" value="{members_text}" style="text;strokeColor=default;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;" vertex="1" parent="{id}">
        <mxGeometry y="60" width="220" height="{members_height}" as="geometry"/>
    </mxCell>
    <mxCell id="{id + 3}" value="{methods_text}" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;" vertex="1" parent="{id}">
        <mxGeometry y="80" width="220" height="{methods_height}" as="geometry"/>
    </mxCell>
"""


def get_responsability_value_height(description: ClassDescription) -> tuple[str, int]:
    # Responsability paragraph
    responsability_text = description.responsability.replace("\n", "&lt;div&gt;")
    responsability_height = responsability_text.count("&lt;div&gt;") * 20 + 10
    responsability_height = max(responsability_height, 20)

    return responsability_text, responsability_height


def get_members_value_height(description: ClassDescription) -> tuple[str, int]:
    # Members paragraph
    members_text = "&lt;div&gt;".join(
        f"{name}: {type_hint}" for name, (type_hint, _) in description.members.items()
    )  # _private: list[str]&amp;nbsp;
    members_height = members_text.count("&lt;div&gt;") * 20 + 10
    members_height = max(members_height, 20)
    return members_text, members_height


def get_methods_value_height(description: ClassDescription) -> tuple[str, int]:
    # Methods paragraph
    methods_text = "&lt;div&gt;".join(
        f"{f.name}({', '.join(f.parameters)}) -&amp;gt; {f.return_typehint}"
        for f in description.methods
    )  # public(param) -&amp;gt; None&lt;div&gt;_private_with_long_name(self) -&amp;gt; None&lt;/div&gt;
    methods_height = methods_text.count("&lt;div&gt;") * 20 + 10
    methods_height = max(methods_height, 20)

    return methods_text, methods_height
