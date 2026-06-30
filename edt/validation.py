from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


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


def _walk_nodes(node: dict[str, Any], page: int | None = None) -> list[tuple[dict[str, Any], int | None]]:
    kind = str(node.get("kind", ""))
    current_page = page
    if kind == "page":
        node_id = str(node.get("id", ""))
        if node_id.startswith("page-"):
            try:
                current_page = int(node_id.removeprefix("page-"))
            except ValueError:
                current_page = page
    nodes = [(node, current_page)]
    children = node.get("children", [])
    if isinstance(children, list):
        for child in children:
            if isinstance(child, dict):
                nodes.extend(_walk_nodes(child, current_page))
    return nodes


def _validate_duplicate_ids(report: ValidationReport, nodes: list[tuple[dict[str, Any], int | None]]) -> None:
    seen: dict[str, int | None] = {}
    for node, page in nodes:
        node_id = str(node.get("id", ""))
        if not node_id:
            continue
        if node_id in seen:
            report.add(ValidationFinding("EDOM010", "error", "structure", f"Duplicate node id: {node_id}", node_id=node_id, page=page))
        else:
            seen[node_id] = page


def _validate_empty_nodes(report: ValidationReport, nodes: list[tuple[dict[str, Any], int | None]]) -> None:
    structural_kinds = {"document", "page"}
    for node, page in nodes:
        kind = str(node.get("kind", ""))
        if kind in structural_kinds:
            continue
        text = str(node.get("text", ""))
        children = node.get("children", [])
        if not text.strip() and (not isinstance(children, list) or not children):
            report.add(ValidationFinding("EDOM011", "warning", "structure", "Node has no text or children.", node_id=str(node.get("id", "")), page=page))


def _validate_page_sequence(report: ValidationReport, root: dict[str, Any]) -> None:
    children = root.get("children", [])
    if not isinstance(children, list):
        return
    page_numbers: list[int] = []
    for child in children:
        if not isinstance(child, dict) or child.get("kind") != "page":
            continue
        node_id = str(child.get("id", ""))
        if not node_id.startswith("page-"):
            report.add(ValidationFinding("EDOM012", "warning", "structure", "Page node id does not follow page-N format.", node_id=node_id))
            continue
        try:
            page_numbers.append(int(node_id.removeprefix("page-")))
        except ValueError:
            report.add(ValidationFinding("EDOM012", "warning", "structure", "Page node id does not contain a valid page number.", node_id=node_id))
    if not page_numbers:
        return
    missing = sorted(set(range(min(page_numbers), max(page_numbers) + 1)) - set(page_numbers))
    for page in missing:
        report.add(ValidationFinding("EDOM013", "error", "structure", f"Missing page {page} in document page sequence.", page=page))


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

    nodes = _walk_nodes(root)
    _validate_duplicate_ids(report, nodes)
    _validate_empty_nodes(report, nodes)
    _validate_page_sequence(report, root)
    return report
