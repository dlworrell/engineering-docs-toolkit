# Importer Architecture

Importers are responsible for acquiring source documents and transforming them into analyzable content suitable for semantic processing.

Importers understand source formats. They do not define document semantics.

## Responsibilities

Importers should:

- Read supported source formats.
- Extract text, images, metadata, and page information.
- Preserve source provenance.
- Produce deterministic intermediate representations.
- Pass extracted content to layout analysis.

## Processing Pipeline

```text
Source document
    -> Format parser
    -> Asset extraction
    -> OCR (when required)
    -> Page model
    -> Layout analysis
```

## Design Principles

- Preserve original evidence.
- Avoid semantic inference.
- Be deterministic.
- Record provenance.
- Fail predictably with actionable diagnostics.

## Supported Sources

Current and planned import sources include:

- PDF
- Markdown
- HTML
- EPUB
- Images (OCR)
- Additional formats through plugins and standards bridges.

## Provenance

Every imported artifact should retain sufficient information to trace semantic objects back to their source document and source region.

## Relationship to EDOM

Importers never construct final semantic meaning directly. Their output feeds layout analysis and semantic recognition, which together produce EDOM.

## Extensibility

New importers should integrate through the importer interface without requiring changes to downstream architecture. Format-specific behavior belongs in importer implementations rather than the semantic core.
