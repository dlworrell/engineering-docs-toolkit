from dataclasses import dataclass, field


@dataclass
class AccessibleTable:
    table_id: str
    caption: str = ""
    headers: list[str] = field(default_factory=list)
    summary: str = ""

    @property
    def has_headers(self) -> bool:
        return bool(self.headers)
