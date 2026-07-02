# EDT Implementation and CLI Audit

**Audit date:** 2026-07-02  
**Audited branch:** `main`  
**Package version:** `0.1.0`

## Purpose

This audit compares EDT's implemented code paths, command-line interface, configuration files, tests, and current documentation claims.

The goal is to establish a factual baseline before writing installation, CLI, configuration, input-format, output-format, and workflow documentation.

## Executive Assessment

EDT contains a substantial collection of tested document-processing components, including:

- A PDF-oriented import pipeline.
- OCR, layout, semantic, and EDOM stages.
- EDOM traversal, lookup, fingerprints, validation, reference graphs, and quality reports.
- Markdown and HTML book output.
- Optional Pandoc-based DOCX and EPUB output.
- Translation-memory and TMX library functions.
- Standards and architecture documentation.

The repository is not yet an integrated EDT 1.0 product.

The principal problem is not the absence of useful components. It is that the components are only partially connected:

- The book build does not consume EDOM.
- The CLI `check` command does not run EDOM validation, the reference graph, or quality reports.
- The import pipeline produces EDOM, but the build pipeline ignores it.
- Several documented inputs and outputs are planned rather than implemented.
- External tool dependencies are not declared or tested end to end.
- Current documentation overstates production readiness in several areas.

The correct immediate milestone is **integration and documentation synchronization**, not adding another isolated subsystem.

## Verified Installation Surface

`pyproject.toml` declares:

- Python 3.11 or later.
- Package name `engineering-docs-toolkit`.
- Package version `0.1.0`.
- Console entry point `edt = edt.cli:main`.
- No Python runtime dependencies.
- No optional dependency groups for OCR, PDF, publishing, or development.

The code also relies conditionally on external executables:

- `pandoc` for DOCX and EPUB output.
- `pdftoppm` for PDF page rendering.
- `tesseract` for OCR when selected.

These dependencies are not currently checked by an installation command or represented in package metadata.

## Verified CLI

The implemented command surface is:

| Command | Current behavior |
| --- | --- |
| `edt` | Runs `build` when no subcommand is supplied |
| `edt build` | Builds a Markdown-source book |
| `edt check` | Scans HTML files in `output/` for two simple accessibility conditions |
| `edt init` | Creates a minimal Markdown-book project |
| `edt import` | Runs the manifest-driven PDF import pipeline |
| `edt import-pdf SOURCE OUTPUT` | Writes a source hash and import-notes file only |
| `edt tm-add DATABASE SOURCE TARGET` | Adds one untyped source-target pair to SQLite |

No CLI command currently exposes:

- Full EDOM validation.
- Reference-graph generation.
- Quality-report generation.
- EDOM-to-HTML publishing.
- TMX import, export, or validation.
- Translation language pairs, reviewer metadata, status, or confidence.
- Dependency diagnostics.
- Profile selection.
- Version reporting.

### CLI behavior requiring documentation

- `edt` with no arguments is equivalent to `edt build`.
- `build`, `check`, and `init` operate on the current working directory.
- `import` defaults to `edt/project.yml`.
- `import-pdf` is not the complete semantic import pipeline.
- `tm-add` initializes the database automatically.

## Project Initialization

`edt init` creates:

```text
source/english/
reference/glossary/
reference/indexes/
book.yaml
```

The generated `book.yaml` contains a title and Markdown/HTML output list.

It does not create:

- `edt/project.yml` for `edt import`.
- A source PDF location.
- Report or page-artifact directories.
- Profiles.
- Assets.
- Cache configuration.
- A sample chapter.
- A project README.

This means the initialized project supports the Markdown book builder but not the documented semantic import workflow without manual setup.

## Configuration Audit

### `book.yaml`

The supported fields are:

| Field | Default |
| --- | --- |
| `title` | `Untitled Engineering Book` |
| `source_dir` | `source/english` |
| `output_dir` | `output` |
| `outputs` | `md`, `html` |

The parser is a deliberately small YAML-like reader. It supports simple scalar strings and indented string lists. It does not implement general YAML types, nested mappings, anchors, quoted-value semantics, or schema validation.

### `edt/project.yml`

The PDF import pipeline recognizes these keys by scanning stripped lines:

| Key | Default |
| --- | --- |
| `primary_pdf` | `source/original/herkules-manual.pdf` |
| `edom` | `output/import/edom` |
| `reports` | `reports/import` |
| `pages` | `pages` |
| `start` | `1` |
| `end` | `start` |
| `engine` | `null` |
| `language` | `eng` |

The parser does not interpret YAML hierarchy. Section names such as `source`, `ocr`, and `outputs` are visual organization only. Duplicate leaf keys in different sections cannot be distinguished reliably.

The HERKULES-specific default source path should not remain a toolkit-wide default.

## Build Pipeline Audit

`edt build` currently:

1. Loads `book.yaml`.
2. Reads all top-level `*.md` files in `source_dir` in lexical filename order.
3. Skips `README.md` content.
4. Concatenates the remaining files.
5. Writes `book.md`.
6. Writes a simple generated `book.html`.
7. Writes `book.hash`.
8. Attempts DOCX and EPUB conversion through Pandoc when requested.
9. Runs glossary and index-summary plugins.
10. Writes `build-manifest.json`.

### Confirmed limitations

- The build does not read EDOM.
- It does not run semantic validation.
- It does not generate a reference graph or quality report.
- It does not use the import report.
- Chapter order is filename order only.
- The HTML renderer supports headings at levels 1 through 3, paragraphs, and custom math replacement. It is not a general Markdown implementation.
- Lists, tables, links, images, fenced code, block quotations, footnotes, and other Markdown constructs are not parsed as structures.
- Markdown and HTML are always generated regardless of the configured output list.
- Unknown output names are ignored.
- Missing Pandoc causes DOCX and EPUB output to be skipped silently.
- The build manifest records configured outputs rather than outputs confirmed to exist.
- The output directory is created without `parents=True`, so a nested output path can fail if its parent does not already exist.

## PDF Import Pipeline Audit

`edt import` is the actual staged import command.

It currently performs:

1. Manifest loading.
2. Source existence and SHA-256 calculation.
3. Source provenance and checksum-file generation.
4. Per-page artifact-directory initialization.
5. PDF page-image extraction through `pdftoppm`.
6. OCR through a null engine or Tesseract.
7. Layout-block generation.
8. Semantic-kind recognition.
9. Semantic-relationship inference and resolution.
10. Per-page EDOM generation.
11. Document EDOM assembly.
12. Import-report generation.
13. A separate PDF import-notes stub.

### Confirmed limitations

- Only PDF is supported by this project importer.
- The default OCR engine is `null`.
- Tesseract output is captured as one plain-text block per page without confidence, bounding boxes, or image dimensions.
- Layout recognition is currently heuristic: caption prefixes and short uppercase text.
- Semantic recognition is primarily prefix- and source-kind-based.
- Tests substitute fake page extraction and fake OCR rather than exercising Poppler and Tesseract end to end.
- The document EDOM is assembled as `document -> page -> block`, making pages structural parents. This conflicts with the documented rule that pages are provenance rather than document structure.
- Imported node identifiers depend on page and block ordinal, so re-pagination or block reordering can change identity.
- The import pipeline is not connected to `edt build`.

### Likely page-render integration defect

The `pdftoppm` invocation uses an output prefix such as `page`, while EDT expects files named like `page-0001.png`.

The unit test mocks `subprocess.run` and does not verify the filenames produced by a real `pdftoppm` process. A real-tool integration test is required, and the extraction code should discover or explicitly normalize actual generated filenames.

## `import-pdf` Command Audit

`edt import-pdf SOURCE OUTPUT` currently:

- Creates the output directory.
- Hashes the source when it exists.
- Writes `import-notes.md`.
- Returns a result with `pages = 0`.

It does not extract pages, OCR content, infer layout, recognize semantics, or produce EDOM.

The command name is therefore misleading. It should be removed, renamed to describe its limited purpose, or made an alias for the full project import pipeline.

## EDOM Audit

The core `EdomNode` supports:

- Kind.
- Text.
- Identifier.
- Children.
- Metadata.
- Recursive fingerprints.
- Child insertion.

Separate modules provide preorder and postorder traversal, lookup by identifier, kind queries, dirty-node comparison, structural checks, JSON conversion, validation, reference graphs, and quality reports.

### Confirmed inconsistencies

- The basic JSON serializer omits node metadata during both serialization and deserialization.
- The EDOM metadata type annotation is `dict[str, str]`, while validation and other code expect booleans, lists, and richer values.
- Page nodes are used as structural parents in imported document EDOM.
- Default node identifiers are random UUIDs, while imported identifiers are page-position-based. A unified stable-identity policy is not implemented.
- The standalone validation, reference-graph, and quality-report modules are not connected to the normal CLI workflow.

## Validation and Quality Audit

The repository contains meaningful library-level validation:

- Missing or invalid document roots.
- Duplicate node identifiers.
- Empty nodes.
- Missing page numbers.
- Theorem and proof adjacency.
- Duplicate semantic numbering.
- Missing or misplaced captions.
- Broken, self, circular, and orphaned references.

It also contains:

- Reference-graph JSON and Markdown output.
- Structural, semantic, reference, and overall quality scores.
- A publication-readiness calculation.

However, `edt check` does not call any of these components.

`edt check` currently scans only `output/*.html` and checks:

- Whether any MathML exists without the substring `alttext=`.
- Whether any image exists without the substring `alt=`.

This implementation can produce false negatives when one image has alternative text and another does not, because it checks the whole file rather than each element. It also ignores a custom `output_dir` from `book.yaml`.

## Translation and TMX Audit

The SQLite translation-memory library supports:

- Source and target text.
- Source and target language.
- Reviewer.
- Status.
- Confidence.
- Origin.
- Review time.

The TMX library supports basic TMX 1.4 import, export, property preservation, XML parsing, and lightweight validation.

Current integration gaps:

- Only the simplest source-target insertion is exposed by the CLI.
- TMX import, export, and validation are not exposed.
- TMX import does not preserve language values when inserting records.
- TMX handling does not preserve full inline-code structure or all multilingual variants.
- No build or localization workflow consumes the translation-memory database.

## Publishing Audit

### Implemented directly

- Concatenated Markdown.
- Simple HTML generated from Markdown-like lines.
- EDOM-to-HTML library renderer.

### Implemented through an external converter

- DOCX through Pandoc.
- EPUB through Pandoc.

### Not integrated as production publishers

- EDOM-driven EPUB.
- PDF output.
- PDF/UA output.
- OOXML profile-driven output.
- ODF output.
- Standards-profile validation.
- Resolved-reference hyperlinks and navigation across all formats.

The EDOM-to-HTML renderer exists as a library function but is not called by `edt build` or exposed by the CLI.

## Test and CI Audit

GitHub Actions currently:

1. Checks out the repository.
2. Installs Python 3.11.
3. Installs the editable package and `pytest`.
4. Runs `make test`.
5. Runs `edt build` in `examples/minimal-book`.
6. Verifies that `output/book.html` exists.

The minimal example requests Markdown, HTML, DOCX, and EPUB, but CI verifies only HTML. Because missing Pandoc is treated as a successful skip, CI does not prove DOCX or EPUB generation.

The current suite provides useful unit coverage but lacks a system-level matrix for:

- Real PDF rendering.
- Real OCR.
- EDOM validation through the CLI.
- Reference and quality reports through the CLI.
- Real Pandoc DOCX and EPUB generation.
- Round-trip office-document behavior.
- Accessibility validation with established validators.
- A complete import-to-publish workflow.

## Documentation Drift

Current documentation contains several claims that are broader than the implemented integrated workflow.

Examples include:

- HTML, EPUB, and translation workflows described as complete.
- Incremental builds described as integrated into normal builds.
- EDOM described as the authoritative build source.
- HTML, EPUB, and OCR image collections listed as current import sources.
- Validation, reference graphs, and quality reports shown as mandatory steps in the first-book workflow.
- Profiles described as operational even though profile-driven semantics remain planned.

These concepts are valid architectural targets, but user documentation must distinguish:

- Implemented and exposed.
- Implemented as a library only.
- Prototype or partial.
- Planned.

## Priority Findings

### P0 — Integrate the product path

1. Define one project configuration model for import, validation, and publication.
2. Make `edt init` create a project that can run the complete supported workflow.
3. Connect imported EDOM to validation, reference graphs, quality reports, and publishers.
4. Replace page-parent document structure with semantic structure plus source-region provenance.
5. Make command failures explicit when requested outputs or dependencies are unavailable.

### P0 — Correct user-facing claims

1. Update README and project status documents to distinguish library capabilities from integrated product capabilities.
2. Document only implemented input and output formats as supported.
3. Mark profile-driven behavior and web snapshots as planned.
4. Explain external dependencies and current parser limitations.

### P1 — Strengthen the CLI

1. Add `edt --version`.
2. Add descriptive help and examples.
3. Add `edt validate` or expand `edt check` to run EDOM validation.
4. Add explicit reference-graph and quality-report commands or outputs.
5. Expose TMX import, export, and validation.
6. Add dependency diagnostics.
7. Make output selection and artifact reporting truthful.

### P1 — Add real integration tests

1. Exercise `pdftoppm` against a fixture PDF.
2. Exercise Tesseract against a controlled image when the dependency is available.
3. Install Pandoc in a publishing CI job and assert DOCX and EPUB files.
4. Run a complete PDF-to-EDOM-to-validation-to-publication fixture.
5. Validate generated EPUB and accessibility structures with external validators.

### P2 — Improve format fidelity

1. Replace the line-based Markdown renderer with a real parser or publish from EDOM.
2. Preserve EDOM metadata in every serializer.
3. Establish stable identifiers independent of page and block position.
4. Add source-region objects that allow semantic nodes to span pages.
5. Introduce versioned mapping profiles for each importer and publisher.

## Recommended Next Work

The next engineering sequence should be:

1. Correct the PDF page-render integration and add a real fixture test.
2. Create a unified project configuration and extend `edt init`.
3. Add a CLI validation pipeline that writes validation, reference, and quality reports.
4. Define a stable, page-independent EDOM document assembly model with source regions.
5. Publish HTML from EDOM.
6. Update README, PROJECT, ROADMAP, and user documentation against the verified command surface.
7. Add DOCX and EPUB integration jobs with declared external dependencies.

## Release Assessment

EDT should continue to identify itself as `0.1.x` while these integration gaps remain.

A defensible EDT 1.0 release requires at least one complete, reproducible workflow in which a supported source is:

```text
initialized
    -> imported
    -> normalized into page-independent EDOM
    -> validated
    -> reference-checked
    -> quality-reported
    -> published
    -> externally validated
```

The repository already contains many of the required parts. The next phase is to connect them into one truthful, testable product path.
