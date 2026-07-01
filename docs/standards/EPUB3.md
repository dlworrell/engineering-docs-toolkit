# EPUB 3

## Purpose

EPUB 3 is the open standard for reflowable digital publications. EDT uses EPUB 3 as a primary publication target for technical books because it supports semantic HTML, accessibility, navigation, embedded media, and packaging.

## Where EDT Uses EPUB 3

- Technical book publication
- Navigation documents and table of contents
- Semantic HTML content
- Accessibility metadata
- Embedded MathML and SVG where supported
- Offline distribution and archival packages

## Where EDT Does Not Use EPUB 3

EPUB 3 is a publication package, not EDT's canonical document model. EDOM remains the authoritative semantic representation used throughout processing.

## Mapping to EDOM

EDOM sections become EPUB content documents, semantic objects are rendered as HTML5, references become internal hyperlinks, and metadata is translated into EPUB package metadata. Provenance remains an internal EDT concern unless explicitly exported.

## Design Notes

EDT generates EPUB from validated EDOM content. Publishers consume semantic structure, reference graphs, and accessibility metadata rather than reconstructing meaning during publication. This keeps EPUB generation deterministic and reproducible.