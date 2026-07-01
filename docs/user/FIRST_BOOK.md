# First Book

This guide introduces the recommended workflow for creating an EDT project and producing a published technical document.

## Goal

Transform source material into a validated, semantic document that can be published into multiple output formats from a single canonical representation.

## Workflow

```text
Collect source material
        ↓
Import into EDT
        ↓
Layout analysis
        ↓
Semantic recognition
        ↓
EDOM
        ↓
Validation
        ↓
Reference graph
        ↓
Quality reports
        ↓
Publication
```

## Typical Inputs

EDT is designed to ingest a variety of source material, including:

- PDF documents
- Markdown
- HTML
- EPUB
- OCR image collections
- Future web snapshots and standards-based importers

## Project Layout

A typical EDT project will contain:

```text
book/
├── sources/
├── assets/
├── profiles/
├── output/
├── reports/
└── cache/
```

## Validation First

Every publication should pass semantic validation before release. Validation ensures structural integrity, semantic consistency, reference completeness, and profile-specific requirements.

## Publish Many

Once a document has been normalized into EDOM, the same semantic source can be rendered into multiple publication formats without re-importing or reinterpreting the original source material.

## Recommended Practice

- Preserve original source material.
- Keep provenance intact.
- Resolve validation findings before publication.
- Treat EDOM as the authoritative semantic source.
- Use profiles to adapt EDT to specific document families instead of modifying the core platform.

This workflow reflects the semantic-first architecture described throughout the EDT documentation.