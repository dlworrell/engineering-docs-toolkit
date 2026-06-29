from dataclasses import dataclass

from .semantic_blocks import SemanticBlock


@dataclass(frozen=True)
class SemanticRelationship:
    source_id: str
    target_id: str
    relationship: str


def link_adjacent_proofs(blocks: list[SemanticBlock]) -> list[SemanticRelationship]:
    relationships: list[SemanticRelationship] = []
    pending_statement: SemanticBlock | None = None
    for block in blocks:
        if block.semantic_kind in {"theorem", "lemma", "proposition", "corollary"}:
            pending_statement = block
        elif block.semantic_kind == "proof" and pending_statement is not None:
            relationships.append(SemanticRelationship(pending_statement.block_id, block.block_id, "has_proof"))
            pending_statement = None
    return relationships
