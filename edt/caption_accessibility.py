from .caption_association import CaptionAssociation
from .figure_alt_text import FigureAltText
from .table_accessibility import AccessibleTable


def figure_alt_from_caption(association: CaptionAssociation) -> FigureAltText:
    return FigureAltText(figure_id=association.content_id, alt_text=association.caption_text)


def table_metadata_from_caption(association: CaptionAssociation) -> AccessibleTable:
    return AccessibleTable(table_id=association.content_id, caption=association.caption_text)
