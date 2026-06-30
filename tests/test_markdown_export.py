from edt.markdown_export import edom_document_to_markdown


def test_edom_document_to_markdown_renders_semantic_nodes():
    payload = {
        "root": {
            "id": "document",
            "kind": "document",
            "children": [
                {
                    "id": "page-1",
                    "kind": "page",
                    "children": [
                        {"id": "h1", "kind": "heading", "text": "HERKULES", "children": []},
                        {"id": "thm1", "kind": "theorem", "text": "Theorem 1.1", "children": []},
                        {"id": "proof1", "kind": "proof", "text": "Proof.", "children": []},
                        {"id": "eq1", "kind": "equation", "text": "x = 1", "children": []},
                    ],
                }
            ],
        }
    }

    markdown = edom_document_to_markdown(payload)

    assert "## HERKULES" in markdown
    assert "**Theorem.** Theorem 1.1" in markdown
    assert "**Proof.** Proof." in markdown
    assert "$$\nx = 1\n$$" in markdown
