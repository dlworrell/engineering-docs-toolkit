# SVG

## Purpose

SVG is the W3C standard for scalable vector graphics. It is important for technical documents because diagrams, schematics, charts, and engineering illustrations often need to remain crisp, searchable, accessible, and resolution-independent.

## Where EDT Uses SVG

- HTML and EPUB publication of vector diagrams.
- Technical illustrations and schematics.
- Charts and generated diagrams.
- Accessibility-aware graphics when metadata is available.
- Future profile-specific diagram rendering.

## Where EDT Does Not Use SVG

SVG is a graphics representation, not EDT's document model. EDOM remains responsible for document semantics, references, captions, provenance, and validation.

## Mapping to EDOM

An EDOM figure may reference an SVG asset. Captions, figure numbers, references, accessibility metadata, and provenance remain EDOM responsibilities.

```text
EDOM figure
    -> SVG asset
    -> caption
    -> references
    -> provenance
```

## Design Notes

EDT should treat SVG as a standards-based asset format for technical graphics. Semantic relationships around the graphic belong in EDOM, while the SVG file represents the rendered vector content.