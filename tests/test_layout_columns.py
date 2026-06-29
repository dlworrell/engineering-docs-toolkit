from edt.layout_columns import column_index, group_two_columns
from edt.layout_model import LayoutBlock


def test_column_index_uses_left_edge():
    block = LayoutBlock(block_id="b1", kind="paragraph", bbox=(25, 0, 50, 10))
    assert column_index(block, split_x=100) == 0


def test_group_two_columns():
    left = LayoutBlock(block_id="l", kind="paragraph", bbox=(0, 0, 50, 10))
    right = LayoutBlock(block_id="r", kind="paragraph", bbox=(150, 0, 200, 10))
    groups = group_two_columns([left, right], split_x=100)
    assert left in groups[0]
    assert right in groups[1]
