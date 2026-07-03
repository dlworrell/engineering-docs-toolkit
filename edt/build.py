import json
from pathlib import Path

from .config import load_config, load_project_config
from .document_reports import generate_document_reports
from .edom_markdown import write_edom_markdown
from .hash_cache import hash_file, hash_text
from .html import markdown_to_html, write_edom_html
from .manifest import write_manifest
from .pandoc import run_pandoc
from .plugin import ProjectContext
from .plugin_registry import default_plugins
from .validation import SEVERITIES, ValidationReport


def _validation_fails(report: ValidationReport, fail_on: str) -> bool:
    threshold = SEVERITIES.index(fail_on)
    return any(
        SEVERITIES.index(finding.severity) >= threshold
        for finding in report.findings
    )


def _write_pandoc_output(book_md: Path, output: Path, format_name: str) -> None:
    if not run_pandoc(book_md, output):
        raise RuntimeError(
            f"requested {format_name} output could not be written: {output}"
        )
    print(f"wrote {output}")


def build_project(root: Path | None = None) -> None:
    root = root or Path.cwd()
    config = load_config(root)
    source = root / config.source_dir
    out = root / config.output_dir
    out.mkdir(exist_ok=True)

    chapters = sorted(source.glob("*.md")) if source.exists() else []
    parts = []
    for chapter in chapters:
        if chapter.name == "README.md":
            continue
        parts.append(chapter.read_text(encoding="utf-8").strip())

    book_text = "\n\n".join(parts) + "\n"
    book_md = out / "book.md"
    book_html = out / "book.html"
    canonical_edom = (
        out / "import" / "edom" / "canonical-document.edom.json"
    )
    document_reports = None
    validation_failure = False
    fail_on = None

    if canonical_edom.exists():
        fingerprint = hash_file(canonical_edom)
        document_payload = json.loads(
            canonical_edom.read_text(encoding="utf-8")
        )
        write_edom_markdown(canonical_edom, book_md)
        write_edom_html(canonical_edom, book_html, title=config.title)
        if (root / "edt.toml").exists():
            project_config = load_project_config(root)
            report_root = root / project_config.paths.reports
            fail_on = project_config.validation.fail_on
        else:
            report_root = root / "reports"
        report_result = generate_document_reports(
            document_payload,
            report_root / "document",
        )
        document_reports = report_result.to_dict()
        if fail_on is not None:
            validation_failure = _validation_fails(
                report_result.validation,
                fail_on,
            )
        source_mode = "canonical-edom"
    else:
        book_md.write_text(book_text, encoding="utf-8")
        fingerprint = hash_text(book_text)
        book_html.write_text(
            markdown_to_html(book_text, config.title),
            encoding="utf-8",
        )
        source_mode = "markdown"

    (out / "book.hash").write_text(fingerprint + "\n", encoding="utf-8")

    print(f"wrote {book_md}")
    print(f"wrote {book_html}")

    if "docx" in config.outputs:
        _write_pandoc_output(book_md, out / "book.docx", "docx")
    if "epub" in config.outputs:
        _write_pandoc_output(book_md, out / "book.epub", "epub")

    context = ProjectContext(root=root, output=out)
    for plugin in default_plugins():
        plugin.run(context)

    manifest = {
        "title": config.title,
        "chapters": len(chapters),
        "fingerprint": fingerprint,
        "outputs": config.outputs,
        "source_mode": source_mode,
    }
    if canonical_edom.exists():
        manifest["canonical_edom"] = str(canonical_edom.relative_to(root))
        manifest["document_reports"] = document_reports
        if fail_on is not None:
            manifest["validation_fail_on"] = fail_on
            manifest["validation_passed"] = not validation_failure
    write_manifest(out, manifest)

    if validation_failure:
        raise RuntimeError(
            f"canonical EDOM validation failed at severity {fail_on}"
        )
