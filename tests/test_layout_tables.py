from edt.layout_model import LayoutBlock
from edt.layout_tables import looks_like_table, table_blocks


def test_table_blocks_filters_table_kind():
    block = LayoutBlock(block_id="t1", kind="table")
    assert table_blocks([block]) == [block]


def test_looks_like_table_detects_pipe_text():
    block = LayoutBlock(block_id="p1", kind="paragraph", text="A | B")
    assert looks_like_table(block)
