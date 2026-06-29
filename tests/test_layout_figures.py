from edt.layout_figures import caption_blocks, figure_blocks
from edt.layout_model import LayoutBlock


def test_figure_blocks_filters_image_kind():
    block = LayoutBlock(block_id="img1", kind="image")
    assert figure_blocks([block]) == [block]


def test_caption_blocks_detects_figure_prefix():
    block = LayoutBlock(block_id="cap1", kind="paragraph", text="Figure 1. Engine")
    assert caption_blocks([block]) == [block]
