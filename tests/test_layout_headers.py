from edt.layout_headers import footer_blocks, header_blocks
from edt.layout_model import LayoutBlock, LayoutPage


def test_header_blocks_use_top_band():
    page = LayoutPage(page_number=1, height=1000)
    block = LayoutBlock(block_id="h", kind="header", bbox=(0, 50, 100, 70))
    page.add_block(block)
    assert header_blocks(page) == [block]


def test_footer_blocks_use_bottom_band():
    page = LayoutPage(page_number=1, height=1000)
    block = LayoutBlock(block_id="f", kind="footer", bbox=(0, 950, 100, 970))
    page.add_block(block)
    assert footer_blocks(page) == [block]
