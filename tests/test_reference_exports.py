from edt.reference_exports import ResolvedLink, resolved_links_from_relationships
from edt.semantic_relationships import SemanticRelationship


def test_resolved_links_filters_reference_relationships():
    relationships = [
        SemanticRelationship(source_id="p1", target_id="eq1", relationship="references"),
        SemanticRelationship(source_id="fig1", target_id="cap1", relationship="has_caption"),
    ]
    assert resolved_links_from_relationships(relationships) == [ResolvedLink(source_id="p1", target_id="eq1")]
