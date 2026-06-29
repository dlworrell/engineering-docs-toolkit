import re
from dataclasses import dataclass


REFERENCE_RE = re.compile(r"\b(?P<kind>Eq\.|Equation|Figure|Table|Theorem)\s*\(?(?P<number>\d+(?:\.\d+)*)\)?", re.IGNORECASE)


@dataclass(frozen=True)
class CrossReference:
    kind: str
    number: str
    text: str

    @property
    def target_id(self) -> str:
        normalized = "equation" if self.kind.lower() in {"eq.", "equation"} else self.kind.lower()
        return f"{normalized}:{self.number}"


def find_cross_references(text: str) -> list[CrossReference]:
    return [CrossReference(kind=match.group("kind"), number=match.group("number"), text=match.group(0)) for match in REFERENCE_RE.finditer(text)]
