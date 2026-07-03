from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .reference_graph import ReferenceGraph
from .validation import ValidationReport


@dataclass(frozen=True)
class QualityReport:
    structural_score: float
    semantic_score: float
    reference_score: float
    overall_score: float
    publication_ready: bool
    errors: int
    warnings: int
    broken_references: int
    orphan_references: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_markdown(self) -> str:
        ready = "YES" if self.publication_ready else "NO"
        return (
            "# EDT Quality Report\n\n"
            f"Structural score: {self.structural_score:.1f}\n"
            f"Semantic score: {self.semantic_score:.1f}\n"
            f"Reference score: {self.reference_score:.1f}\n"
            f"Overall score: {self.overall_score:.1f}\n\n"
            f"Publication ready: {ready}\n\n"
            f"Errors: {self.errors}\n"
            f"Warnings: {self.warnings}\n"
            f"Broken references: {self.broken_references}\n"
            f"Orphan references: {self.orphan_references}\n"
        )

    def write_json(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return path

    def write_markdown(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_markdown(), encoding="utf-8")
        return path


def _score_from_findings(
    validation_report: ValidationReport,
    category: str,
) -> float:
    errors = sum(
        1
        for finding in validation_report.findings
        if finding.category == category and finding.severity == "error"
    )
    warnings = sum(
        1
        for finding in validation_report.findings
        if finding.category == category and finding.severity == "warning"
    )
    score = 100.0 - (errors * 25.0) - (warnings * 5.0)
    return max(0.0, score)


def build_quality_report(
    validation_report: ValidationReport,
    reference_graph: ReferenceGraph,
) -> QualityReport:
    structural_score = _score_from_findings(validation_report, "structure")
    semantic_score = _score_from_findings(validation_report, "semantic")
    reference_score = _score_from_findings(validation_report, "reference")
    overall_score = round(
        (structural_score + semantic_score + reference_score) / 3.0,
        1,
    )
    graph_payload = reference_graph.to_dict()["summary"]
    broken_references = int(graph_payload["broken"])
    orphan_references = int(graph_payload["orphans"])
    has_document_content = any(
        node.kind != "document" for node in reference_graph.nodes.values()
    )
    publication_ready = (
        has_document_content
        and validation_report.error_count == 0
        and broken_references == 0
        and overall_score >= 90.0
    )
    return QualityReport(
        structural_score=round(structural_score, 1),
        semantic_score=round(semantic_score, 1),
        reference_score=round(reference_score, 1),
        overall_score=overall_score,
        publication_ready=publication_ready,
        errors=validation_report.error_count,
        warnings=validation_report.warning_count,
        broken_references=broken_references,
        orphan_references=orphan_references,
    )
