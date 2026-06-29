import re
from dataclasses import dataclass


REFERENCE_RE = re.compile(r"\b(?P<kind>Eq\.|Equation|Figure|Table|Theorem)\s*\(?(?P<number>\d+(?:\.\d+)*)\)?", re.IGNORECASE)


KIND_TARGETS = {
    "eq.": "equation",
    "equation": "equation",
    "figure": "figure",
    "table": "table",
    "theorem": "theorem",
}


@dataclass(frozen=True)
class CrossReference:
    kind: str
    number: str
    text: str

    @property
    def target_kind(self) -> str:
        return KIND_TARGETS[self.kind.lower()]

    @property
    def target_id(self) -> str:
        return f"{self.target_kind}:{self.number}"


def find_cross_references(text: str) -> list[CrossReference]:
    return [CrossReference(kind=match.group("kind"), number=match.group("number"), text=match.group(0)) for match in REFERENCE_RE.finditer(text)]
