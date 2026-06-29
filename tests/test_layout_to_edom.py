from edt.layout_model import LayoutBlock, LayoutPage
from edt.layout_to_edom import block_to_edom, page_to_edom


def test_block_to_edom_maps_paragraph():
    block = LayoutBlock(block_id="b1", kind="paragraph", text="Hello")
    node = block_to_edom(block)
    assert node.kind == "paragraph"
    assert node.text == "Hello"


def test_page_to_edom_adds_ordered_blocks():
    page = LayoutPage(page_number=1)
    page.add_block(LayoutBlock(block_id="b2", kind="paragraph", text="Second", bbox=(0, 20, 10, 30)))
    page.add_block(LayoutBlock(block_id="b1", kind="paragraph", text="First", bbox=(0, 10, 10, 20)))
    node = page_to_edom(page)
    assert node.children[0].text == "First"
