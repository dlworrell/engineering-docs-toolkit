from .reference_index import build_reference_index
from .semantic_blocks import SemanticBlock
from .semantic_relationships import SemanticRelationship


def resolve_reference_relationships(blocks: list[SemanticBlock], relationships: list[SemanticRelationship]) -> list[SemanticRelationship]:
    index = build_reference_index(blocks)
    resolved: list[SemanticRelationship] = []
    for relationship in relationships:
        if relationship.relationship == "references" and relationship.target_id in index:
            resolved.append(SemanticRelationship(relationship.source_id, index[relationship.target_id], "references"))
        else:
            resolved.append(relationship)
    return resolved
