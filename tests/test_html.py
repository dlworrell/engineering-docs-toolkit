from edt.html import edom_document_to_html, markdown_to_html


def test_math_survives_html_escape():
    html = markdown_to_html("# Title\n\nArea $a^2$", "Test")
    assert "<math" in html
    assert "&lt;math" not in html


def test_edom_document_to_html_renders_semantic_nodes():
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
                    ],
                }
            ],
        }
    }

    html = edom_document_to_html(payload, title="HERKULES")

    assert "<title>HERKULES</title>" in html
    assert 'id="page-1" data-edt-kind="page" class="edt-page"' in html
    assert 'id="h1" data-edt-kind="heading"' in html
    assert 'class="edt-theorem"' in html
    assert 'class="edt-proof"' in html
