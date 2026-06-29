from edt.caption_accessibility import figure_alt_from_caption, table_metadata_from_caption
from edt.caption_association import CaptionAssociation


def test_figure_alt_from_caption():
    association = CaptionAssociation(content_id="fig1", caption_id="cap1", caption_text="Figure 1. Engine")
    assert figure_alt_from_caption(association).alt_text == "Figure 1. Engine"


def test_table_metadata_from_caption():
    association = CaptionAssociation(content_id="tab1", caption_id="cap1", caption_text="Table 1. Values")
    assert table_metadata_from_caption(association).caption == "Table 1. Values"
