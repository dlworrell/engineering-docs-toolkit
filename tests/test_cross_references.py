from edt.cross_references import find_cross_references


def test_find_equation_cross_reference():
    refs = find_cross_references("See Eq. (2.3) for the result.")
    assert refs[0].kind == "Eq."
    assert refs[0].number == "2.3"
    assert refs[0].target_id == "equation:2.3"


def test_find_figure_cross_reference():
    refs = find_cross_references("See Figure 1.2.")
    assert refs[0].target_id == "figure:1.2"


def test_find_table_cross_reference():
    refs = find_cross_references("See Table 3.4.")
    assert refs[0].target_id == "table:3.4"


def test_find_equation_word_cross_reference():
    refs = find_cross_references("Equation (2.3) gives the identity.")
    assert refs[0].target_id == "equation:2.3"


def test_find_theorem_cross_reference():
    refs = find_cross_references("Use Theorem 4.1.")
    assert refs[0].target_id == "theorem:4.1"
