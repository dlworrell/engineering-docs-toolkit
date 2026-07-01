# MathML

## Purpose

MathML is the W3C standard for representing mathematical notation in a structured, machine-readable form. It preserves the semantics of mathematical expressions while supporting high-quality rendering, accessibility, search, and interchange.

## Where EDT Uses MathML

- Canonical representation of mathematical expressions during publication.
- Accessible HTML and EPUB output.
- Screen reader support.
- Searchable and semantically meaningful mathematics.
- Interoperability with standards-compliant publishing systems.

## Where EDT Does Not Use MathML

MathML is not the internal semantic model for an entire document. EDOM remains the canonical document representation. MathML represents mathematical content within that model.

## Mapping to EDOM

EDOM equation nodes may contain or reference MathML representations. Equation numbering, references, proofs, and provenance remain EDOM responsibilities, while MathML captures the mathematical expression itself.

## Design Notes

EDT should preserve mathematical meaning from import through publication. When source formats contain LaTeX, OCR-recognized equations, or other mathematical notation, the long-term goal is to normalize expressions into MathML for standards-based publication while retaining provenance back to the original source.