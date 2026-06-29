from edt.caption_association import associate_figures_with_captions, associate_tables_with_captions
from edt.layout_model import LayoutBlock, LayoutPage


def test_associate_figures_with_captions():
    page = LayoutPage(page_number=1)
    page.add_block(LayoutBlock(block_id="fig1", kind="figure", bbox=(0, 10, 100, 100)))
    page.add_block(LayoutBlock(block_id="cap1", kind="caption", text="Figure 1. Engine", bbox=(0, 110, 100, 130)))
    result = associate_figures_with_captions(page)
    assert result[0].caption_text == "Figure 1. Engine"


def test_associate_tables_with_captions():
    page = LayoutPage(page_number=1)
    page.add_block(LayoutBlock(block_id="tab1", kind="table", bbox=(0, 10, 100, 100)))
    page.add_block(LayoutBlock(block_id="cap1", kind="caption", text="Table 1. Values", bbox=(0, 110, 100, 130)))
    result = associate_tables_with_captions(page)
    assert result[0].content_id == "tab1"
