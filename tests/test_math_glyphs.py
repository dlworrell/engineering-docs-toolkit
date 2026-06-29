from edt.math_glyphs import contains_math_glyph, is_math_glyph, math_range_for


def test_math_glyph_detects_operator():
    assert is_math_glyph("∑")


def test_math_glyph_detects_arrow():
    assert is_math_glyph("→")


def test_math_range_for_math_alphabet():
    assert math_range_for(chr(0x1D538)) == "Mathematical Alphanumeric Symbols"


def test_contains_math_glyph_detects_expression():
    assert contains_math_glyph("x ∈ A")
