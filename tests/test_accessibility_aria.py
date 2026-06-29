from edt.accessibility_aria import AriaAnnotation, aria_attributes


def test_aria_attributes_include_role_and_label():
    annotation = AriaAnnotation(role="img", label="diagram")
    attrs = aria_attributes(annotation)
    assert attrs["role"] == "img"
    assert attrs["aria-label"] == "diagram"
