# Publisher Architecture

Publishers render EDOM into target output formats.

Publishers consume semantic document data. They do not infer semantics from text, layout, or presentation.

## Responsibilities

Publishers are responsible for:

- Rendering EDOM into target formats.
- Preserving document structure.
- Generating stable anchors and links.
- Emitting accessibility metadata when supported.
- Including captions, references, tables, figures, equations, and semantic blocks.
- Producing deterministic output suitable for regression testing.

## Non-Responsibilities

Publishers should not:

- Perform OCR.
- Infer headings or semantic blocks.
- Resolve references from prose.
- Repair broken document structure.
- Reclassify layout elements.

Those tasks belong upstream in import, layout analysis, semantic recognition, validation, and reference graph construction.

## Processing Model

```text
EDOM
    -> Publisher
    -> Output format
```

Publisher-specific processing may include format adaptation, asset copying, navigation generation, stylesheet generation, and metadata emission.

## Current Output Families

EDT currently supports or is designed around these publication targets:

- HTML
- Markdown
- EPUB
- PDF-oriented workflows
- Future DOCX and standards-oriented outputs

## Reference Integration

Publishers should use stable EDOM identifiers and reference graph data to generate:

- HTML anchors
- EPUB navigation
- Cross-reference links
- Figure and table links
- Equation links
- Backlinks where supported

## Accessibility

Publishers should preserve accessibility metadata whenever the target format supports it, including:

- Heading hierarchy
- Figure alt text
- Table structure
- MathML or equation metadata
- ARIA annotations where appropriate
- EPUB accessibility metadata

## Determinism

Publisher output should be deterministic for the same EDOM input, configuration, and assets. Deterministic output supports regression testing, release validation, and reproducible publication workflows.

## Relationship to Profiles

Profiles may influence publisher behavior through document-family-specific conventions such as numbering, labels, captions, glossary handling, warning blocks, theorem environments, or service-manual procedure formatting.

Profiles should configure publisher behavior without requiring each publisher to hard-code every document family.

## Long-Term Direction

Future publishers may target additional formats, standards, archival packages, web documentation sites, static books, and evidence-preserving publication bundles. The publisher contract should remain centered on EDOM as the canonical input.