from edt.layout_model import LayoutBlock
from edt.layout_paragraphs import paragraph_blocks, paragraph_text


def test_paragraph_blocks_filters_and_orders():
    second = LayoutBlock(block_id="p2", kind="paragraph", text="Second", bbox=(0, 20, 10, 30))
    first = LayoutBlock(block_id="p1", kind="paragraph", text="First", bbox=(0, 10, 10, 20))
    assert paragraph_blocks([second, first])[0].text == "First"


def test_paragraph_text_joins_paragraphs():
    blocks = [LayoutBlock(block_id="p1", kind="paragraph", text="First"), LayoutBlock(block_id="p2", kind="paragraph", text="Second")]
    assert paragraph_text(blocks) == "First\n\nSecond"
