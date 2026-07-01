# EDT Architecture Handbook

This handbook describes the architecture of the Engineering Documents Toolkit (EDT), a semantic document engineering platform.

The architecture follows the project charter, vision, and manifesto:

- [Project Charter](../../PROJECT_CHARTER.md)
- [Vision](../vision/VISION.md)
- [Semantic Document Engineering Manifesto](../vision/MANIFESTO.md)

## Architectural Thesis

A document is not a sequence of pages. It is a semantic knowledge structure with traceable provenance.

EDT therefore separates source presentation from semantic meaning. Source formats are imported, analyzed, and normalized into the Engineering Document Object Model (EDOM). Downstream systems validate, enrich, translate, and publish from that canonical representation.

## System Pipeline

```text
Source material
    -> Importer
    -> OCR / extraction
    -> Layout analysis
    -> Semantic recognition
    -> EDOM
    -> Validation
    -> Reference graph
    -> Quality report
    -> Publishers
```

## Primary Subsystems

### Importers

Importers acquire source material and convert it into analyzable document data. Importers are responsible for format-specific extraction, not final document semantics.

### OCR and Page Extraction

OCR and page extraction preserve source evidence and produce text, image, and page models suitable for layout analysis.

### Layout Analysis

Layout analysis identifies visual structures such as blocks, headings, figures, tables, captions, columns, notes, and equations.

### Semantic Recognition

Semantic recognition converts layout structures into document meaning: sections, definitions, theorems, proofs, figures, tables, examples, exercises, references, and related technical objects.

### EDOM

The Engineering Document Object Model is EDT's canonical semantic representation. It preserves document structure, semantic meaning, metadata, references, accessibility information, and provenance.

### Validation

Validation operates on EDOM. It checks structural integrity, semantic integrity, captions, numbering, references, orphaned objects, and publication readiness.

### Reference Graph

The reference graph records incoming references, outgoing references, broken links, orphaned objects, and graph statistics for addressable document objects.

### Quality Reports

Quality reports summarize validation and reference graph data into publication-readiness metrics.

### Publishers

Publishers render EDOM into output formats. Publishers do not infer semantics; they consume the semantic model produced upstream.

## Design Principles

- Semantics before presentation.
- Pages are provenance, not structure.
- Importers normalize source formats.
- Publishers render semantic models.
- Validation checks meaning.
- Provenance is preserved throughout the pipeline.
- Standards are adopted where practical.
- Profiles extend document semantics without modifying the core platform.

## Planned Handbook Sections

- EDOM
- Provenance
- Importers
- OCR
- Layout
- Semantics
- Validation
- Reference graph
- Quality reports
- Publishers
- Profiles
- Standards integration
