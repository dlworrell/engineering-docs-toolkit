from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import ConfigError, load_project_config
from .edom import EdomNode
from .edom_json import node_to_dict
from .hash_cache import hash_file, hash_text
from .layout_model import LayoutBlock, LayoutPage
from .ocr_engine import NullOcrEngine, OcrEngine
from .ocr_model import OcrBlock, OcrPage
from .ocr_to_layout import ocr_page_to_layout
from .pdf_import import import_pdf
from .pdf_pages import extract_pdf_pages
from .reference_resolver import resolve_reference_relationships
from .semantic_blocks import SemanticBlock
from .semantic_document import SemanticDocument, SemanticPage, semantic_page_from_layout
from .semantic_relationships import SemanticRelationship, infer_semantic_relationships
from .semantic_to_edom import (
    semantic_document_to_canonical_edom,
    semantic_page_to_edom,
)
from .tesseract_ocr import TesseractOcrEngine


@dataclass
class ProjectImportConfig:
    manifest: Path
    source_pdf: Path
    output_dir: Path
    report_dir: Path
    pages_dir: Path
    first_page: int
    last_page: int
    ocr_engine: str
    ocr_language: str


@dataclass
class ProjectImportResult:
    config: ProjectImportConfig
    source_exists: bool
    fingerprint: str
    report_path: Path


def _read_manifest_value(manifest: Path, key: str) -> str | None:
    if not manifest.exists():
        return None
    prefix = f"{key}:"
    for raw_line in manifest.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith(prefix):
            return line[len(prefix) :].strip().strip('"').strip("'")
    return None


def _read_manifest_int(manifest: Path, key: str, default: int) -> int:
    value = _read_manifest_value(manifest, key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _load_unified_import_config(root: Path) -> ProjectImportConfig:
    project = load_project_config(root)
    pdf_source = project.first_source("pdf")
    if pdf_source is None:
        raise ConfigError(
            "edt.toml must define a source with type = \"pdf\" for edt import"
        )

    return ProjectImportConfig(
        manifest=root / "edt.toml",
        source_pdf=root / pdf_source.path,
        output_dir=root / project.paths.output / "import" / "edom",
        report_dir=root / project.paths.reports / "import",
        pages_dir=root / project.paths.work / "pages",
        first_page=project.import_settings.first_page,
        last_page=project.import_settings.last_page,
        ocr_engine=project.import_settings.ocr_engine,
        ocr_language=project.import_settings.ocr_language,
    )


def load_project_import_config(
    root: Path,
    manifest: Path | None = None,
) -> ProjectImportConfig:
    if manifest is None and (root / "edt.toml").exists():
        return _load_unified_import_config(root)

    manifest_path = manifest or root / "edt" / "project.yml"
    if not manifest_path.is_absolute():
        manifest_path = root / manifest_path

    source_value = _read_manifest_value(manifest_path, "primary_pdf") or "source/original/herkules-manual.pdf"
    edom_value = _read_manifest_value(manifest_path, "edom") or "output/import/edom"
    reports_value = _read_manifest_value(manifest_path, "reports") or "reports/import"
    pages_value = _read_manifest_value(manifest_path, "pages") or "pages"
    first_page = _read_manifest_int(manifest_path, "start", 1)
    last_page = _read_manifest_int(manifest_path, "end", first_page)
    ocr_engine = _read_manifest_value(manifest_path, "engine") or "null"
    ocr_language = _read_manifest_value(manifest_path, "language") or "eng"

    return ProjectImportConfig(
        manifest=manifest_path,
        source_pdf=root / source_value,
        output_dir=root / edom_value,
        report_dir=root / reports_value,
        pages_dir=root / pages_value,
        first_page=first_page,
        last_page=max(first_page, last_page),
        ocr_engine=ocr_engine,
        ocr_language=ocr_language,
    )


def write_source_provenance(root: Path, source_pdf: Path, fingerprint: str) -> None:
    source_dir = source_pdf.parent
    source_dir.mkdir(parents=True, exist_ok=True)
    checksum_path = source_dir / "SHA256SUMS"
    provenance_path = source_dir / "provenance.md"
    checksum_path.write_text(f"{fingerprint}  {source_pdf.name}\n", encoding="utf-8")
    provenance_path.write_text(
        "# Source Provenance\n\n"
        f"Canonical source: `{source_pdf.relative_to(root)}`\n\n"
        f"SHA-256: `{fingerprint}`\n\n"
        "This file records the canonical source artifact used by the EDT import pipeline.\n",
        encoding="utf-8",
    )


def page_artifact_dir(pages_dir: Path, page_number: int) -> Path:
    return pages_dir / f"{page_number:04d}"


def is_pdf_file(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        return path.read_bytes()[:5] == b"%PDF-"
    except OSError:
        return False


def _update_page_manifest(path: Path, **updates: object) -> None:
    page_manifest = json.loads(path.read_text(encoding="utf-8"))
    page_manifest.update(updates)
    path.write_text(json.dumps(page_manifest, indent=2) + "\n", encoding="utf-8")


def initialize_page_artifacts(root: Path, config: ProjectImportConfig, fingerprint: str, source_exists: bool) -> list[dict[str, object]]:
    config.pages_dir.mkdir(parents=True, exist_ok=True)
    pages: list[dict[str, object]] = []
    for page_number in range(config.first_page, config.last_page + 1):
        artifact_dir = page_artifact_dir(config.pages_dir, page_number)
        artifact_dir.mkdir(parents=True, exist_ok=True)
        page_manifest = {
            "page": page_number,
            "source_pdf": str(config.source_pdf.relative_to(root)),
            "source_sha256": fingerprint,
            "source_exists": source_exists,
            "artifacts": {
                "image": str((artifact_dir / "image.png").relative_to(root)),
                "ocr": str((artifact_dir / "ocr.json").relative_to(root)),
                "layout": str((artifact_dir / "layout.json").relative_to(root)),
                "semantic": str((artifact_dir / "semantic.json").relative_to(root)),
                "edom": str((artifact_dir / "edom.json").relative_to(root)),
            },
            "status": "waiting_for_source_pdf" if not source_exists else "initialized",
            "image_status": "waiting_for_source_pdf" if not source_exists else "pending",
            "ocr_status": "waiting_for_image",
            "layout_status": "waiting_for_ocr",
            "semantic_status": "waiting_for_layout",
            "edom_status": "waiting_for_semantic",
        }
        (artifact_dir / "manifest.json").write_text(json.dumps(page_manifest, indent=2) + "\n", encoding="utf-8")
        pages.append(
            {
                "page": page_number,
                "directory": str(artifact_dir.relative_to(root)),
                "status": page_manifest["status"],
                "image_status": page_manifest["image_status"],
                "ocr_status": page_manifest["ocr_status"],
                "layout_status": page_manifest["layout_status"],
                "semantic_status": page_manifest["semantic_status"],
                "edom_status": page_manifest["edom_status"],
            }
        )
    return pages


def extract_page_images(root: Path, config: ProjectImportConfig, source_exists: bool) -> list[dict[str, object]]:
    if not source_exists:
        return []
    if not is_pdf_file(config.source_pdf):
        results = []
        for page_number in range(config.first_page, config.last_page + 1):
            manifest_path = page_artifact_dir(config.pages_dir, page_number) / "manifest.json"
            _update_page_manifest(manifest_path, image_status="skipped_not_pdf")
            results.append({"page": page_number, "status": "skipped_not_pdf"})
        return results

    render_dir = config.pages_dir / "_rendered"
    results: list[dict[str, object]] = []
    try:
        rendered_pages = extract_pdf_pages(config.source_pdf, render_dir, config.first_page, config.last_page)
    except (OSError, subprocess.CalledProcessError) as exc:
        for page_number in range(config.first_page, config.last_page + 1):
            manifest_path = page_artifact_dir(config.pages_dir, page_number) / "manifest.json"
            _update_page_manifest(manifest_path, image_status="extract_failed", image_error=str(exc))
            results.append({"page": page_number, "status": "extract_failed", "error": str(exc)})
        return results

    for rendered_page in rendered_pages:
        artifact_dir = page_artifact_dir(config.pages_dir, rendered_page.page_number)
        target_image = artifact_dir / "image.png"
        if rendered_page.image_path.exists():
            shutil.copyfile(rendered_page.image_path, target_image)
            image_status = "extracted"
        else:
            image_status = "extract_missing_output"
        manifest_path = artifact_dir / "manifest.json"
        _update_page_manifest(manifest_path, image_status=image_status)
        results.append({"page": rendered_page.page_number, "status": image_status, "image": str(target_image.relative_to(root))})
    return results


def make_ocr_engine(config: ProjectImportConfig) -> OcrEngine:
    if config.ocr_engine == "tesseract":
        return TesseractOcrEngine(language=config.ocr_language)
    return NullOcrEngine()


def run_ocr(root: Path, config: ProjectImportConfig, engine: OcrEngine) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for page_number in range(config.first_page, config.last_page + 1):
        artifact_dir = page_artifact_dir(config.pages_dir, page_number)
        image_path = artifact_dir / "image.png"
        ocr_path = artifact_dir / "ocr.json"
        manifest_path = artifact_dir / "manifest.json"
        if not image_path.exists():
            _update_page_manifest(manifest_path, ocr_status="waiting_for_image")
            results.append({"page": page_number, "status": "waiting_for_image"})
            continue
        try:
            page = engine.recognize_image(image_path, page_number=page_number)
            ocr_payload = {
                "page": page.page_number,
                "engine": getattr(engine, "name", "ocr"),
                "image": str(image_path.relative_to(root)),
                "width": page.width,
                "height": page.height,
                "text": page.text,
                "blocks": [asdict(block) for block in page.blocks],
            }
            ocr_path.write_text(json.dumps(ocr_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            _update_page_manifest(manifest_path, ocr_status="complete")
            results.append({"page": page_number, "status": "complete", "ocr": str(ocr_path.relative_to(root))})
        except (OSError, subprocess.CalledProcessError) as exc:
            _update_page_manifest(manifest_path, ocr_status="failed", ocr_error=str(exc))
            results.append({"page": page_number, "status": "failed", "error": str(exc)})
    return results


def _ocr_page_from_payload(payload: dict[str, object]) -> OcrPage:
    page = OcrPage(page_number=int(payload["page"]), width=int(payload.get("width", 0)), height=int(payload.get("height", 0)))
    for block in payload.get("blocks", []):
        if not isinstance(block, dict):
            continue
        bbox = block.get("bbox")
        if isinstance(bbox, list):
            bbox = tuple(bbox)
        page.blocks.append(OcrBlock(text=str(block.get("text", "")), confidence=float(block.get("confidence", 0.0)), bbox=bbox))
    return page


def generate_layouts(root: Path, config: ProjectImportConfig) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for page_number in range(config.first_page, config.last_page + 1):
        artifact_dir = page_artifact_dir(config.pages_dir, page_number)
        ocr_path = artifact_dir / "ocr.json"
        layout_path = artifact_dir / "layout.json"
        manifest_path = artifact_dir / "manifest.json"
        if not ocr_path.exists():
            _update_page_manifest(manifest_path, layout_status="waiting_for_ocr")
            results.append({"page": page_number, "status": "waiting_for_ocr"})
            continue
        payload = json.loads(ocr_path.read_text(encoding="utf-8"))
        layout = ocr_page_to_layout(_ocr_page_from_payload(payload))
        layout_payload = {
            "page": layout.page_number,
            "width": layout.width,
            "height": layout.height,
            "source_ocr": str(ocr_path.relative_to(root)),
            "blocks": [asdict(block) for block in layout.blocks],
        }
        layout_path.write_text(json.dumps(layout_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        _update_page_manifest(manifest_path, layout_status="complete")
        results.append({"page": page_number, "status": "complete", "layout": str(layout_path.relative_to(root)), "blocks": len(layout.blocks)})
    return results


def _layout_page_from_payload(payload: dict[str, object]) -> LayoutPage:
    page = LayoutPage(page_number=int(payload["page"]), width=int(payload.get("width", 0)), height=int(payload.get("height", 0)))
    for block in payload.get("blocks", []):
        if not isinstance(block, dict):
            continue
        bbox = block.get("bbox")
        if isinstance(bbox, list):
            bbox = tuple(bbox)
        page.add_block(
            LayoutBlock(
                block_id=str(block.get("block_id", "")),
                kind=str(block.get("kind", "paragraph")),
                text=str(block.get("text", "")),
                bbox=bbox,
                confidence=float(block.get("confidence", 0.0)),
            )
        )
    return page


def generate_semantics(root: Path, config: ProjectImportConfig) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for page_number in range(config.first_page, config.last_page + 1):
        artifact_dir = page_artifact_dir(config.pages_dir, page_number)
        layout_path = artifact_dir / "layout.json"
        semantic_path = artifact_dir / "semantic.json"
        manifest_path = artifact_dir / "manifest.json"
        if not layout_path.exists():
            _update_page_manifest(manifest_path, semantic_status="waiting_for_layout")
            results.append({"page": page_number, "status": "waiting_for_layout"})
            continue
        layout_payload = json.loads(layout_path.read_text(encoding="utf-8"))
        semantic_page = semantic_page_from_layout(_layout_page_from_payload(layout_payload))
        relationships = infer_semantic_relationships(semantic_page)
        semantic_payload = {
            "page": semantic_page.page_number,
            "source_layout": str(layout_path.relative_to(root)),
            "blocks": [asdict(block) for block in semantic_page.blocks],
            "relationships": [asdict(relationship) for relationship in relationships],
        }
        semantic_path.write_text(json.dumps(semantic_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        _update_page_manifest(manifest_path, semantic_status="complete")
        results.append({"page": page_number, "status": "complete", "semantic": str(semantic_path.relative_to(root)), "blocks": len(semantic_page.blocks), "relationships": len(relationships)})
    return results


def _semantic_block_from_payload(payload: dict[str, object]) -> SemanticBlock:
    return SemanticBlock(
        block_id=str(payload.get("block_id", "")),
        kind=str(payload.get("kind", "paragraph")),
        text=str(payload.get("text", "")),
        metadata={str(key): value for key, value in dict(payload.get("metadata", {})).items()},
    )


def _semantic_page_from_payload(payload: dict[str, object]) -> SemanticPage:
    page = SemanticPage(page_number=int(payload["page"]))
    for block in payload.get("blocks", []):
        if isinstance(block, dict):
            page.blocks.append(_semantic_block_from_payload(block))
    return page


def _relationship_from_payload(payload: dict[str, object]) -> SemanticRelationship:
    return SemanticRelationship(
        relationship=str(payload.get("relationship", "")),
        source_id=str(payload.get("source_id", "")),
        target_id=str(payload.get("target_id", "")),
        metadata={str(key): value for key, value in dict(payload.get("metadata", {})).items()},
    )


def _edom_node_to_payload(node: EdomNode) -> dict[str, object]:
    return {
        "id": node.node_id,
        "kind": node.kind,
        "text": node.text,
        "metadata": node.metadata,
        "children": [_edom_node_to_payload(child) for child in node.children],
    }


def generate_page_edom(root: Path, config: ProjectImportConfig) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for page_number in range(config.first_page, config.last_page + 1):
        artifact_dir = page_artifact_dir(config.pages_dir, page_number)
        semantic_path = artifact_dir / "semantic.json"
        edom_path = artifact_dir / "edom.json"
        manifest_path = artifact_dir / "manifest.json"
        if not semantic_path.exists():
            _update_page_manifest(manifest_path, edom_status="waiting_for_semantic")
            results.append({"page": page_number, "status": "waiting_for_semantic"})
            continue
        semantic_payload = json.loads(semantic_path.read_text(encoding="utf-8"))
        semantic_page = _semantic_page_from_payload(semantic_payload)
        relationships = [
            _relationship_from_payload(item)
            for item in semantic_payload.get("relationships", [])
            if isinstance(item, dict)
        ]
        resolved_relationships = resolve_reference_relationships(semantic_page, relationships)
        edom = semantic_page_to_edom(semantic_page, resolved_relationships)
        edom_payload = {
            "page": page_number,
            "source_semantic": str(semantic_path.relative_to(root)),
            "root": _edom_node_to_payload(edom),
            "relationships": [asdict(relationship) for relationship in resolved_relationships],
        }
        edom_path.write_text(json.dumps(edom_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        _update_page_manifest(manifest_path, edom_status="complete", status="complete")
        results.append({"page": page_number, "status": "complete", "edom": str(edom_path.relative_to(root)), "nodes": len(edom.children)})
    return results


def assemble_document_edom(root: Path, config: ProjectImportConfig) -> dict[str, object]:
    config.output_dir.mkdir(parents=True, exist_ok=True)
    document = EdomNode(kind="document", node_id="document")
    imported_pages = 0
    for page_number in range(config.first_page, config.last_page + 1):
        edom_path = page_artifact_dir(config.pages_dir, page_number) / "edom.json"
        if not edom_path.exists():
            continue
        edom_payload = json.loads(edom_path.read_text(encoding="utf-8"))
        page_root = edom_payload.get("root")
        if not isinstance(page_root, dict):
            continue
        page_node = EdomNode(kind="page", node_id=f"page-{page_number}", metadata={"page_number": page_number})
        for child_payload in page_root.get("children", []):
            if not isinstance(child_payload, dict):
                continue
            page_node.add(
                EdomNode(
                    kind=str(child_payload.get("kind", "paragraph")),
                    text=str(child_payload.get("text", "")),
                    node_id=str(child_payload.get("id", "")) or None,
                    metadata={str(key): value for key, value in dict(child_payload.get("metadata", {})).items()},
                )
            )
        document.add(page_node)
        imported_pages += 1

    output_path = config.output_dir / "document.edom.json"
    document_payload = {
        "source_pdf": str(config.source_pdf.relative_to(root)),
        "page_range": {"start": config.first_page, "end": config.last_page},
        "imported_pages": imported_pages,
        "root": _edom_node_to_payload(document),
    }
    output_path.write_text(json.dumps(document_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "status": "complete" if imported_pages else "waiting_for_page_edom",
        "document": str(output_path.relative_to(root)),
        "pages": imported_pages,
    }


def assemble_canonical_document_edom(
    root: Path,
    config: ProjectImportConfig,
) -> dict[str, object]:
    config.output_dir.mkdir(parents=True, exist_ok=True)
    document = SemanticDocument()
    imported_pages = 0

    for page_number in range(config.first_page, config.last_page + 1):
        semantic_path = page_artifact_dir(config.pages_dir, page_number) / "semantic.json"
        if not semantic_path.exists():
            continue
        semantic_payload = json.loads(semantic_path.read_text(encoding="utf-8"))
        document.add_page(_semantic_page_from_payload(semantic_payload))
        imported_pages += 1

    document.infer_relationships()
    canonical = semantic_document_to_canonical_edom(
        document,
        source_id="primary",
    )
    canonical.metadata.update(
        {
            "source_pdf": str(config.source_pdf.relative_to(root)),
            "page_range": {
                "start": config.first_page,
                "end": config.last_page,
            },
        }
    )

    output_path = config.output_dir / "canonical-document.edom.json"
    output_path.write_text(
        json.dumps({"root": node_to_dict(canonical)}, indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    return {
        "status": "complete" if imported_pages else "waiting_for_semantics",
        "document": str(output_path.relative_to(root)),
        "pages": imported_pages,
        "nodes": len(canonical.children),
    }


def import_project(root: Path, manifest: Path | None = None, engine: OcrEngine | None = None) -> ProjectImportResult:
    config = load_project_import_config(root, manifest)
    source_exists = config.source_pdf.exists()
    fingerprint = hash_file(config.source_pdf) if source_exists else "missing"
    write_source_provenance(root, config.source_pdf, fingerprint)
    pages = initialize_page_artifacts(root, config, fingerprint, source_exists)
    images = extract_page_images(root, config, source_exists)
    ocr_results = run_ocr(root, config, engine or make_ocr_engine(config))
    layout_results = generate_layouts(root, config)
    semantic_results = generate_semantics(root, config)
    page_edom_results = generate_page_edom(root, config)
    document_edom_result = assemble_document_edom(root, config)
    canonical_document_edom_result = assemble_canonical_document_edom(root, config)
    import_result = None
    config.report_dir.mkdir(parents=True, exist_ok=True)
    if source_exists:
        import_result = import_pdf(config.source_pdf, config.output_dir)
    report = {
        "status": "source_ready" if source_exists else "waiting_for_source_pdf",
        "manifest": str(config.manifest.relative_to(root)),
        "source_pdf": str(config.source_pdf.relative_to(root)),
        "source_exists": source_exists,
        "source_sha256": fingerprint,
        "page_range": {"start": config.first_page, "end": config.last_page},
        "ocr": {"engine": config.ocr_engine, "language": config.ocr_language},
        "output_dir": str(config.output_dir.relative_to(root)),
        "pages_dir": str(config.pages_dir.relative_to(root)),
        "pages": pages,
        "image_results": images,
        "ocr_results": ocr_results,
        "layout_results": layout_results,
        "semantic_results": semantic_results,
        "page_edom_results": page_edom_results,
        "document_edom": document_edom_result,
        "canonical_document_edom": canonical_document_edom_result,
        "import_result": {
            "source": str(import_result.source.relative_to(root)),
            "output_dir": str(import_result.output_dir.relative_to(root)),
            "pages": import_result.pages,
            "source_hash": import_result.source_hash,
        }
        if import_result is not None
        else None,
    }
    report_path = config.report_dir / "import-report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return ProjectImportResult(config=config, source_exists=source_exists, fingerprint=fingerprint, report_path=report_path)
