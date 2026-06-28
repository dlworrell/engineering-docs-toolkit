from edt.math_parser import replace_math


def test_inline_math():
    html = replace_math("Let $x+1$ be positive.")
    assert "<math" in html
    assert "x+1" in html


def test_display_math():
    html = replace_math("$$x^2$$")
    assert 'display="block"' in html
