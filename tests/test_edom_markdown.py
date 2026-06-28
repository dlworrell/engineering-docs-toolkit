from edt.edom_markdown import markdown_to_edom


def test_markdown_to_edom():
    doc = markdown_to_edom("# Intro\nHello")
    assert doc.kind == "document"
    assert doc.children[0].kind == "heading1"
    assert doc.children[0].children[0].text == "Hello"
