from dataclasses import dataclass, field


@dataclass
class BuildGraph:
    edges: dict[str, set[str]] = field(default_factory=dict)

    def add_node(self, node_id: str) -> None:
        self.edges.setdefault(node_id, set())

    def add_edge(self, node_id: str, upstream_id: str) -> None:
        self.add_node(node_id)
        self.add_node(upstream_id)
        self.edges[node_id].add(upstream_id)

    def upstream_of(self, node_id: str) -> set[str]:
        return set(self.edges.get(node_id, set()))
