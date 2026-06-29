from edt.layout_model import LayoutBlock
from edt.reading_order import top_left_order


def test_top_left_order_sorts_by_vertical_position():
    lower = LayoutBlock(block_id="b2", kind="paragraph", bbox=(0, 20, 10, 30))
    upper = LayoutBlock(block_id="b1", kind="paragraph", bbox=(0, 10, 10, 20))
    assert top_left_order([lower, upper])[0].block_id == "b1"
