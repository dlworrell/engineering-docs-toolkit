from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


SEVERITIES = ("info", "warning", "error")


@dataclass(frozen=True)
class ValidationFinding:
    rule: str
    severity: str
    category: str
    message: str
    node_id: str = ""
    page: int | None = None

    def __post_init__(self) -> None:
        if self.severity not in SEVERITIES:
            raise ValueError(f"invalid severity: {self.severity}")


@dataclass
class ValidationReport:
    findings: list[ValidationFinding] = field(default_factory=list)

    def add(self, finding: ValidationFinding) -> None:
        self.findings.append(finding)

    @property
    def error_count(self) -> int:
        return sum(1 for finding in self.findings if finding.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for finding in self.findings if finding.severity == "warning")

    @property
    def info_count(self) -> int:
        return sum(1 for finding in self.findings if finding.severity == "info")

    def to_dict(self) -> dict[str, object]:
        return {
            "summary": {
                "findings": len(self.findings),
                "errors": self.error_count,
                "warnings": self.warning_count,
                "info": self.info_count,
            },
            "findings": [asdict(finding) for finding in self.findings],
        }

    def to_markdown(self) -> str:
        lines = [
            "# EDT Validation Report",
            "",
            f"Findings: {len(self.findings)}",
            f"Errors: {self.error_count}",
            f"Warnings: {self.warning_count}",
            f"Info: {self.info_count}",
            "",
        ]
        if not self.findings:
            lines.append("No validation findings.")
            return "\n".join(lines) + "\n"

        lines.append("| Severity | Rule | Category | Page | Node | Message |")
        lines.append("|---|---|---|---:|---|---|")
        for finding in self.findings:
            page = "" if finding.page is None else str(finding.page)
            node = finding.node_id.replace("|", "\\|")
            message = finding.message.replace("|", "\\|")
            lines.append(f"| {finding.severity} | {finding.rule} | {finding.category} | {page} | {node} | {message} |")
        return "\n".join(lines) + "\n"

    def write_json(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return path

    def write_markdown(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_markdown(), encoding="utf-8")
        return path


def validate_document_edom(document_payload: dict[str, object]) -> ValidationReport:
    report = ValidationReport()
    root = document_payload.get("root")
    if not isinstance(root, dict):
        report.add(ValidationFinding("EDOM001", "error", "structure", "Document EDOM has no root node."))
        return report
    if root.get("kind") != "document":
        report.add(ValidationFinding("EDOM002", "error", "structure", "Root node is not a document node.", node_id=str(root.get("id", ""))))
    children = root.get("children", [])
    if not isinstance(children, list) or not children:
        report.add(ValidationFinding("EDOM003", "warning", "structure", "Document has no page children.", node_id=str(root.get("id", ""))))
    return report
