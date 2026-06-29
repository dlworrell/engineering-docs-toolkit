from dataclasses import dataclass

from .semantic_relationships import SemanticRelationship


@dataclass(frozen=True)
class ResolvedLink:
    source_id: str
    target_id: str


def resolved_links_from_relationships(relationships: list[SemanticRelationship]) -> list[ResolvedLink]:
    return [ResolvedLink(source_id=relationship.source_id, target_id=relationship.target_id) for relationship in relationships if relationship.relationship == "references"]
