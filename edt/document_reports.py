from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .quality import QualityReport, build_quality_report
from .reference_graph import ReferenceGraph, build_reference_graph
from .validation import ValidationReport, validate_document_edom


@dataclass(frozen=True)
class DocumentReportResult:
    validation: ValidationReport
    reference_graph: ReferenceGraph
    quality: QualityReport
    report_dir: Path

    def to_dict(self) -> dict[str, object]:
        return {
            "validation": {
                "errors": self.validation.error_count,
                "warnings": self.validation.warning_count,
                "info": self.validation.info_count,
                "json": str(self.report_dir / "validation.json"),
                "markdown": str(self.report_dir / "validation.md"),
            },
            "reference_graph": {
                **self.reference_graph.to_dict()["summary"],
                "json": str(self.report_dir / "reference-graph.json"),
                "markdown": str(self.report_dir / "reference-graph.md"),
            },
            "quality": {
                **self.quality.to_dict(),
                "json": str(self.report_dir / "quality.json"),
                "markdown": str(self.report_dir / "quality.md"),
            },
        }


def generate_document_reports(
    document_payload: dict[str, object],
    report_dir: Path,
) -> DocumentReportResult:
    """Validate canonical EDOM and write reference and quality reports."""

    validation = validate_document_edom(document_payload)
    reference_graph = build_reference_graph(document_payload)
    quality = build_quality_report(validation, reference_graph)

    report_dir.mkdir(parents=True, exist_ok=True)
    validation.write_json(report_dir / "validation.json")
    validation.write_markdown(report_dir / "validation.md")
    reference_graph.write_json(report_dir / "reference-graph.json")
    reference_graph.write_markdown(report_dir / "reference-graph.md")
    quality.write_json(report_dir / "quality.json")
    quality.write_markdown(report_dir / "quality.md")

    return DocumentReportResult(
        validation=validation,
        reference_graph=reference_graph,
        quality=quality,
        report_dir=report_dir,
    )
