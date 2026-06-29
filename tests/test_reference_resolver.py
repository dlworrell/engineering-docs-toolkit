from edt.reference_resolver import resolve_reference_relationships
from edt.semantic_blocks import SemanticBlock
from edt.semantic_relationships import SemanticRelationship


def test_resolve_reference_relationship_to_block_id():
    equation = SemanticBlock(block_id="eq1", semantic_kind="equation", text="x = 1", metadata={"equation_number": "2.3"})
    relationship = SemanticRelationship(source_id="p1", target_id="equation:2.3", relationship="references")
    resolved = resolve_reference_relationships([equation], [relationship])
    assert resolved[0].target_id == "eq1"


def test_unresolved_reference_relationship_is_preserved():
    relationship = SemanticRelationship(source_id="p1", target_id="equation:9.9", relationship="references")
    resolved = resolve_reference_relationships([], [relationship])
    assert resolved[0].target_id == "equation:9.9"
