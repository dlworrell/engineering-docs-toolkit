from edt.edom_markdown import edom_document_to_markdown, markdown_to_edom


def test_markdown_to_edom():
    doc = markdown_to_edom("# Intro\nHello")
    assert doc.kind == "document"
    assert doc.children[0].kind == "heading1"
    assert doc.children[0].children[0].text == "Hello"


def test_edom_document_to_markdown():
    markdown = edom_document_to_markdown(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "title",
                        "kind": "title",
                        "text": "HERKULES",
                        "children": [],
                    },
                    {
                        "id": "h1",
                        "kind": "heading",
                        "text": "Theory",
                        "metadata": {"level": 2},
                        "children": [],
                    },
                    {
                        "id": "p1",
                        "kind": "paragraph",
                        "text": "Canonical semantic content.",
                        "children": [],
                    },
                    {
                        "id": "eq1",
                        "kind": "equation",
                        "text": "x = 1",
                        "children": [],
                    },
                    {
                        "id": "proof1",
                        "kind": "proof",
                        "text": "Immediate.",
                        "children": [],
                    },
                ],
            }
        }
    )

    assert markdown == (
        "# HERKULES\n"
        "\n"
        "## Theory\n"
        "\n"
        "Canonical semantic content.\n"
        "\n"
        "$$\n"
        "x = 1\n"
        "$$\n"
        "\n"
        "### Proof\n"
        "\n"
        "Immediate.\n"
    )
