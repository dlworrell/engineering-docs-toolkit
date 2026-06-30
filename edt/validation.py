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


def _node_number(node: dict[str, Any]) -> str:
    metadata = node.get("metadata", {})
    if not isinstance(metadata, dict):
        return ""
    value = metadata.get("number", metadata.get("equation_number", ""))
    return str(value).strip()


def _node_references(node: dict[str, Any]) -> list[str]:
    metadata = node.get("metadata", {})
    if not isinstance(metadata, dict):
        return []
    value = metadata.get("references", metadata.get("reference", metadata.get("target_id", "")))
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    return []


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


def _validate_theorem_proof_pairs(report: ValidationReport, nodes: list[tuple[dict[str, Any], int | None]]) -> None:
    linear = [(node, page) for node, page in nodes if str(node.get("kind", "")) not in {"document", "page"}]
    for index, (node, page) in enumerate(linear):
        kind = str(node.get("kind", ""))
        node_id = str(node.get("id", ""))
        if kind == "theorem":
            next_kind = str(linear[index + 1][0].get("kind", "")) if index + 1 < len(linear) else ""
            if next_kind != "proof":
                report.add(ValidationFinding("SEM001", "warning", "semantic", "Theorem is not immediately followed by a proof.", node_id=node_id, page=page))
        if kind == "proof":
            previous_kind = str(linear[index - 1][0].get("kind", "")) if index > 0 else ""
            if previous_kind != "theorem":
                report.add(ValidationFinding("SEM002", "warning", "semantic", "Proof is not immediately preceded by a theorem.", node_id=node_id, page=page))


def _validate_duplicate_numbers(report: ValidationReport, nodes: list[tuple[dict[str, Any], int | None]]) -> None:
    rules = {
        "theorem": "SEM010",
        "figure": "SEM011",
        "table": "SEM012",
        "definition": "SEM013",
    }
    seen: dict[tuple[str, str], tuple[str, int | None]] = {}
    for node, page in nodes:
        kind = str(node.get("kind", ""))
        if kind not in rules:
            continue
        number = _node_number(node)
        if not number:
            continue
        key = (kind, number)
        node_id = str(node.get("id", ""))
        if key in seen:
            report.add(ValidationFinding(rules[kind], "warning", "semantic", f"Duplicate {kind} number: {number}", node_id=node_id, page=page))
        else:
            seen[key] = (node_id, page)


def _has_caption_child(node: dict[str, Any]) -> bool:
    children = node.get("children", [])
    if not isinstance(children, list):
        return False
    return any(isinstance(child, dict) and child.get("kind") == "caption" for child in children)


def _validate_captions(report: ValidationReport, nodes: list[tuple[dict[str, Any], int | None]]) -> None:
    valid_caption_owners = {"figure", "table", "listing", "equation"}
    for node, page in nodes:
        kind = str(node.get("kind", ""))
        node_id = str(node.get("id", ""))
        if kind == "figure" and not _has_caption_child(node):
            report.add(ValidationFinding("SEM020", "warning", "semantic", "Figure is missing a caption.", node_id=node_id, page=page))
        if kind == "table" and not _has_caption_child(node):
            report.add(ValidationFinding("SEM021", "warning", "semantic", "Table is missing a caption.", node_id=node_id, page=page))

        children = node.get("children", [])
        if not isinstance(children, list):
            continue
        for child in children:
            if isinstance(child, dict) and child.get("kind") == "caption" and kind not in valid_caption_owners:
                report.add(ValidationFinding("SEM022", "warning", "semantic", "Caption is attached to a node that cannot own captions.", node_id=str(child.get("id", "")), page=page))


def _validate_references(report: ValidationReport, nodes: list[tuple[dict[str, Any], int | None]]) -> None:
    node_ids = {str(node.get("id", "")) for node, _page in nodes if str(node.get("id", ""))}
    adjacency: dict[str, list[str]] = {}
    for node, page in nodes:
        node_id = str(node.get("id", ""))
        if not node_id:
            continue
        references = _node_references(node)
        adjacency[node_id] = references
        for target_id in references:
            if target_id not in node_ids:
                report.add(ValidationFinding("REF001", "warning", "reference", f"Reference target does not exist: {target_id}", node_id=node_id, page=page))
            if target_id == node_id:
                report.add(ValidationFinding("REF003", "warning", "reference", "Node references itself.", node_id=node_id, page=page))

    visited: set[str] = set()
    visiting: set[str] = set()

    def visit(node_id: str) -> bool:
        if node_id in visiting:
            return True
        if node_id in visited:
            return False
        visiting.add(node_id)
        for target_id in adjacency.get(node_id, []):
            if target_id in node_ids and visit(target_id):
                return True
        visiting.remove(node_id)
        visited.add(node_id)
        return False

    for node_id in adjacency:
        if visit(node_id):
            report.add(ValidationFinding("REF003", "warning", "reference", "Circular reference detected.", node_id=node_id))
            break


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
    _validate_theorem_proof_pairs(report, nodes)
    _validate_duplicate_numbers(report, nodes)
    _validate_captions(report, nodes)
    _validate_references(report, nodes)
    return report
