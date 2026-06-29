from edt.layout_model import LayoutBlock, LayoutPage


def test_layout_page_adds_block():
    page = LayoutPage(page_number=1)
    block = page.add_block(LayoutBlock(block_id="b1", kind="paragraph", text="Hello"))
    assert block.text == "Hello"
    assert len(page.blocks) == 1
