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


def test_literal_math_element_in_text_is_escaped():
    # EDT-001: a <math> element typed into document text must not pass through.
    payload = {"root": {"id": "p", "kind": "paragraph", "text": '<math x="1"><script>alert(1)</script></math>'}}
    html = edom_document_to_html(payload)
    assert "<script>" not in html
    assert "&lt;math x=&quot;1&quot;&gt;&lt;script&gt;" in html


def test_markup_inside_math_delimiters_is_escaped():
    html = markdown_to_html("Area $<script>alert(1)</script>$ and $$</math><img src=x onerror=alert(1)>$$", "Test")
    assert "<script>" not in html
    assert "<img" not in html
    assert html.count("<math ") == 2


def test_inline_and_display_math_render_with_escaped_text_between():
    from edt.html import render_inline

    assert render_inline("a < b $x$ & $$y$$ c") == (
        'a &lt; b <math xmlns="http://www.w3.org/1998/Math/MathML" alttext="x"><mtext>x</mtext></math> &amp; '
        '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block" alttext="y"><mtext>y</mtext></math> c'
    )
