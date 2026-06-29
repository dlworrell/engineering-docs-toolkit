from edt.cross_references import find_cross_references


def test_find_equation_cross_reference():
    refs = find_cross_references("See Eq. (2.3) for the result.")
    assert refs[0].kind == "Eq."
    assert refs[0].number == "2.3"
    assert refs[0].target_id == "equation:2.3"


def test_find_figure_cross_reference():
    refs = find_cross_references("See Figure 1.2.")
    assert refs[0].target_id == "figure:1.2"
