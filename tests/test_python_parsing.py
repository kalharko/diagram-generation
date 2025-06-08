from diagram_generation.python.class_description import ClassDescription


def test_python_class_parsing() -> None:
    source = """
asdfa
asdf
aa

class A(B, C):
    \"\"\"Dummy docstring
    Responsabilities:
    - Dummy responsability

    end of docstring.
    \"\"\"

    member: member_typehint  # member_doc

    @decorator
    @second(decorator)
    def __init__(self, a: list[a_typehint], b: b_typehing) -> return_val:
        pass
"""

    class_description = ClassDescription(source)
    assert class_description.name == "A"
    assert (
        class_description.docstring
        == """Dummy docstring
    Responsabilities:
    - Dummy responsability

    end of docstring.
    """
    )
    assert class_description.base_classes == ["B", "C"]
    assert class_description.method_names == ["__init__"]
    assert class_description.members == {"member": ("member_typehint", "member_doc")}

    method0 = class_description.methods[0]
    assert method0.name == "__init__"
    assert method0.docstring == ""
    assert method0.return_values == ["return_val"]
    assert method0.parameters == {
        "self": None,
        "a": "list[a_typehint]",
        "b": "b_typehing",
    }
    assert method0.decorators == ["decorator", "second(decorator)"]
