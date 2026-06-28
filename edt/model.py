from dataclasses import dataclass, field


@dataclass
class Section:
    level: int
    title: str
    body: list[str] = field(default_factory=list)


@dataclass
class Document:
    title: str
    sections: list[Section] = field(default_factory=list)
