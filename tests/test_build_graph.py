from edt.build_graph import BuildGraph


def test_build_graph_starts_empty():
    build_graph = BuildGraph()
    build_graph.add_node("node-a")
    result = build_graph.upstream_of("node-a")
    assert len(result) == 0
