from edt.semantic_mathml import mathml, mi, mn, mo, mrow


def test_semantic_mathml_wraps_expression():
    expression = mathml(mrow(mi("x"), mo("="), mn(1)))
    assert expression.startswith("<math")
    assert "<mi>x</mi>" in expression
