from edt.figure_alt_text import FigureAltText


def test_figure_alt_text_completeness():
    figure = FigureAltText(figure_id="fig-1", alt_text="Engine diagram")
    assert figure.is_complete
