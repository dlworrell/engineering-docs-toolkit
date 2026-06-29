from dataclasses import dataclass

from .cross_references import find_cross_references
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


def link_adjacent_captions(blocks: list[SemanticBlock]) -> list[SemanticRelationship]:
    relationships: list[SemanticRelationship] = []
    for index, block in enumerate(blocks):
        if block.semantic_kind not in {"figure", "table"}:
            continue
        candidates = blocks[max(0, index - 1) : index] + blocks[index + 1 : index + 2]
        for candidate in candidates:
            if candidate.semantic_kind == "caption":
                relationships.append(SemanticRelationship(block.block_id, candidate.block_id, "has_caption"))
                break
    return relationships


def link_equation_numbers(blocks: list[SemanticBlock]) -> list[SemanticRelationship]:
    relationships: list[SemanticRelationship] = []
    for block in blocks:
        number = block.metadata.get("equation_number", "")
        if block.semantic_kind == "equation" and number:
            relationships.append(SemanticRelationship(block.block_id, f"equation-number:{number}", "has_number"))
    return relationships


def link_cross_references(blocks: list[SemanticBlock]) -> list[SemanticRelationship]:
    relationships: list[SemanticRelationship] = []
    for block in blocks:
        for reference in find_cross_references(block.text):
            relationships.append(SemanticRelationship(block.block_id, reference.target_id, "references"))
    return relationships


def infer_semantic_relationships(blocks: list[SemanticBlock]) -> list[SemanticRelationship]:
    return link_adjacent_proofs(blocks) + link_adjacent_captions(blocks) + link_equation_numbers(blocks) + link_cross_references(blocks)
