from edt.edom import EdomNode
from edt.edom_reference_metadata import add_reference_metadata, find_edom_node
from edt.reference_exports import ResolvedLink


def test_find_edom_node_finds_nested_node():
    root = EdomNode(kind="document", node_id="document")
    child = root.add(EdomNode(kind="paragraph", node_id="p1"))
    assert find_edom_node(root, "p1") == child


def test_add_reference_metadata_to_source_node():
    root = EdomNode(kind="document", node_id="document")
    paragraph = root.add(EdomNode(kind="paragraph", node_id="p1"))
    add_reference_metadata(root, [ResolvedLink(source_id="p1", target_id="eq1")])
    assert paragraph.metadata["references"] == "eq1"
