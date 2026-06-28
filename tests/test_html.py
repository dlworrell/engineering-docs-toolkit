from edt.html import markdown_to_html


def test_math_survives_html_escape():
    html = markdown_to_html("# Title\n\nArea $a^2$", "Test")
    assert "<math" in html
    assert "&lt;math" not in html
