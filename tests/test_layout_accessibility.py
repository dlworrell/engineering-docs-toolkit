from edt.layout_accessibility import aria_for_block, alt_text_for_figure, accessible_table_for_block
from edt.layout_model import LayoutBlock


def test_aria_for_figure_block():
    block = LayoutBlock(block_id="fig1", kind="figure", text="Diagram")
    assert aria_for_block(block).role == "figure"


def test_alt_text_for_figure_uses_block_text():
    block = LayoutBlock(block_id="fig1", kind="figure", text="Engine diagram")
    assert alt_text_for_figure(block).alt_text == "Engine diagram"


def test_accessible_table_for_block_reads_header_row():
    block = LayoutBlock(block_id="table1", kind="table", text="Part | Value\nA | B")
    table = accessible_table_for_block(block)
    assert table.headers == ["Part", "Value"]
