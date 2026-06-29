from .layout_model import LayoutBlock


PROOF_END_MARKERS = {"qed", "□", "■", "∎"}


def proof_end_marker(block: LayoutBlock) -> str:
    text = block.text.strip()
    for marker in PROOF_END_MARKERS:
        if text.endswith(marker):
            return marker
    return ""


def has_proof_end_marker(block: LayoutBlock) -> bool:
    return bool(proof_end_marker(block))
