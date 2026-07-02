import json
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from .hash_cache import hash_text
from .source_region import SourceRegion


@dataclass
class EdomNode:
    kind: str
    text: str = ""
    node_id: str = field(default_factory=lambda: str(uuid4()))
    children: list["EdomNode"] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    source_regions: list[SourceRegion] = field(default_factory=list)

    @property
    def fingerprint(self) -> str:
        child_hashes = "".join(child.fingerprint for child in self.children)
        metadata_json = json.dumps(
            self.metadata,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        regions_json = json.dumps(
            [region.to_dict() for region in self.source_regions],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hash_text(
            f"{self.kind}\n{self.text}\n{metadata_json}\n{regions_json}\n{child_hashes}"
        )

    def add(self, child: "EdomNode") -> "EdomNode":
        self.children.append(child)
        return child

    def add_source_region(self, region: SourceRegion) -> SourceRegion:
        self.source_regions.append(region)
        return region
