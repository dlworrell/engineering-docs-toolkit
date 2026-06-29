from edt.reference_numbers import add_reference_number_metadata, reference_number_from_text
from edt.semantic_blocks import SemanticBlock


def test_reference_number_from_figure_text():
    assert reference_number_from_text("Figure 1.2 Engine diagram", "figure") == "1.2"


def test_reference_number_from_table_text():
    assert reference_number_from_text("Table 3.4 Values", "table") == "3.4"


def test_reference_number_from_theorem_text():
    assert reference_number_from_text("Theorem 4.1", "theorem") == "4.1"


def test_add_reference_number_metadata():
    block = SemanticBlock(block_id="fig1", semantic_kind="figure", text="Figure 1.2 Engine diagram")
    add_reference_number_metadata(block)
    assert block.metadata["number"] == "1.2"
