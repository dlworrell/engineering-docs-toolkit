from edt.layout_model import LayoutBlock, LayoutPage
from edt.layout_notes import footnote_blocks, marginalia_blocks


def test_footnote_blocks_filter_kind():
    page = LayoutPage(page_number=1)
    block = LayoutBlock(block_id="n1", kind="footnote")
    page.add_block(block)
    assert footnote_blocks(page) == [block]


def test_marginalia_blocks_use_page_edges():
    page = LayoutPage(page_number=1, width=1000)
    block = LayoutBlock(block_id="m1", kind="note", bbox=(950, 10, 990, 40))
    page.add_block(block)
    assert marginalia_blocks(page) == [block]
