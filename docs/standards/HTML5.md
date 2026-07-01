# HTML5

## Purpose

HTML5 is the primary open standard for publishing structured documents on the web. EDT uses HTML5 as a major publication target because it supports semantic elements, accessibility, hyperlinking, and long-term interoperability.

## Where EDT Uses HTML5

- Primary web publishing output
- Semantic headings and document structure
- Navigation and hyperlinks
- Tables and figures
- Accessibility metadata
- Embedded MathML and SVG where supported

## Where EDT Does Not Use HTML5

HTML5 is an output format, not EDT's internal semantic representation. EDOM remains the canonical document model.

## Mapping to EDOM

EDOM semantic objects map naturally to HTML5 elements where appropriate:

| EDOM | HTML5 |
|------|-------|
| document | `<html>` |
| section | `<section>` |
| paragraph | `<p>` |
| figure | `<figure>` |
| caption | `<figcaption>` |
| table | `<table>` |
| quotation | `<blockquote>` |

More specialized semantic objects, such as theorems and proofs, are represented through semantic markup, classes, ARIA attributes, or profile-specific conventions.

## Design Notes

EDT publishes standards-compliant HTML while preserving semantic meaning, accessibility, stable identifiers, and provenance-derived traceability where appropriate. HTML5 is a publication target, not the source of document semantics.