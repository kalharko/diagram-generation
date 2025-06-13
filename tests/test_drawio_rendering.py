from diagram_generation.drawio.generate import (
    class_full_drawio_table,
    get_members_value_height,
    get_methods_value_height,
    get_responsability_value_height,
)
from diagram_generation.drawio.update import update_drawio
from diagram_generation.python.class_description import ClassDescription
from diagram_generation.python.function_description import FunctionDescription


def test_drawio_rendering() -> None:
    class_description = ClassDescription(
        source="",
    )
    class_description.name = "A"
    class_description.docstring = "A docstring\nResponsabilities:\n- A responsability"
    class_description.base_classes = ["B", "C"]
    class_description.members = {"member": ("member_typehint", "member_doc")}
    func_description = FunctionDescription(source="")
    func_description.name = "func"
    func_description.parameters = {"a": "a_typehint", "b": "b_typehint"}
    func_description.return_typehint = "return_typehint"
    class_description.methods = [func_description]

    # Generation
    responsability_text, responsability_height = get_responsability_value_height(
        class_description
    )
    members_text, members_height = get_members_value_height(class_description)
    methods_text, methods_height = get_methods_value_height(class_description)

    xml = class_full_drawio_table(class_description, 0)

    # Assertion
    assert responsability_text == "Responsabilities:&lt;div&gt;- A responsability"
    assert members_text == "member: member_typehint"
    assert methods_text == "func(a, b) -&amp;gt; return_typehint"
    assert (
        xml
        == f"""<mxCell id="0" value="{class_description.name}" style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
        <mxGeometry x="60" y="180" width="220" height="110" as="geometry"/>
    </mxCell>
    <mxCell id="1" value="{responsability_text}" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;" vertex="1" parent="0">
        <mxGeometry y="30" width="220" height="{responsability_height}" as="geometry"/>
    </mxCell>
    <mxCell id="2" value="{members_text}" style="text;strokeColor=default;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;" vertex="1" parent="0">
        <mxGeometry y="60" width="220" height="{members_height}" as="geometry"/>
    </mxCell>
    <mxCell id="3" value="{methods_text}" style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;" vertex="1" parent="0">
        <mxGeometry y="80" width="220" height="{methods_height}" as="geometry"/>
    </mxCell>
"""
    )


def test_update() -> None:
    class_description = ClassDescription(
        source="",
    )
    class_description.name = "A"
    class_description.docstring = "A docstring\nResponsabilities:\n- A responsability"
    class_description.base_classes = ["B", "C"]
    class_description.members = {"member": ("member_typehint", "member_doc")}
    func_description = FunctionDescription(source="")
    func_description.name = "func"
    func_description.parameters = {"a": "a_typehint", "b": "b_typehint"}
    func_description.return_typehint = "return_typehint"
    class_description.methods = [func_description]

    xml = class_full_drawio_table(class_description, 0)

    updated_xml = update_drawio(current_xml=xml, class_descriptions=[class_description])

    assert xml == updated_xml
