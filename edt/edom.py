from dataclasses import dataclass, field
from uuid import uuid4

from .hash_cache import hash_text


@dataclass
class EdomNode:
    kind: str
    text: str = ""
    node_id: str = field(default_factory=lambda: str(uuid4()))
    children: list["EdomNode"] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def fingerprint(self) -> str:
        child_hashes = "".join(child.fingerprint for child in self.children)
        metadata_hash = "".join(f"{key}={value}\n" for key, value in sorted(self.metadata.items()))
        return hash_text(f"{self.kind}\n{self.text}\n{metadata_hash}\n{child_hashes}")

    def add(self, child: "EdomNode") -> "EdomNode":
        self.children.append(child)
        return child
