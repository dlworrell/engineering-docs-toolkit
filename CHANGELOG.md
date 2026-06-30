# Changelog

This changelog records project-level engineering milestones for Engineering Docs Toolkit (EDT). It is intentionally organized by capability rather than by every individual commit.

## Unreleased

### Documentation

- Updated project documentation to describe EDT as a semantic document-understanding and publication engine.
- Added current status, roadmap, completion estimates, and downstream project guidance.
- Clarified that book-specific assets such as the HERKULES manual belong in their own book repositories rather than in EDT.

## v0.8 - Semantic relationships and reference resolution

### Added

- Semantic relationship model.
- Theorem, lemma, proposition, and corollary linkage to adjacent proofs.
- Figure and table caption relationship promotion.
- Equation number relationships.
- Cross-reference detection for forms such as:
  - `Figure 1.2`
  - `Table 3.4`
  - `Equation (2.3)`
  - `Eq. (2.3)`
  - `Theorem 4.1`
- Reference index builder for equations, figures, tables, and theorems.
- Reference resolver that rewrites textual reference targets into semantic block identifiers when possible.
- Resolved reference export model.
- EDOM reference metadata helper.
- Semantic-to-EDOM propagation of resolved reference metadata.

### Improved

- Semantic blocks now preserve metadata through EDOM conversion.
- EDOM fingerprints now account for metadata.
- Equations, proof markers, and reference numbers are carried into semantic metadata.

## v0.7 - Semantic recognition layer

### Added

- Semantic block model.
- Semantic document and semantic page models.
- Recognition for:
  - titles
  - authors
  - chapters
  - sections
  - headings
  - definitions
  - theorems
  - lemmas
  - corollaries
  - propositions
  - proofs
  - examples
  - exercises
  - algorithms
  - captions
  - figures
  - tables
  - equations
  - code listings
  - quotations
  - citations
  - bibliography and index blocks
- Equation number extraction.
- Proof-end marker extraction, including `qed`, `□`, `■`, and `∎`.
- Unicode mathematical glyph registry covering common mathematical Unicode ranges and ASCII operators.

## v0.6 - Accessibility pipeline

### Added

- ARIA annotation helpers.
- Semantic accessibility role mapping.
- Equation accessibility labels.
- Figure alt-text support.
- Table accessibility metadata.
- EPUB accessibility metadata.
- MathML generation support.
- Accessibility reporting.

### Improved

- Captions can seed figure alt text and table metadata.
- Equation numbers can contribute to accessible equation labels.

## v0.5 - OCR framework

### Added

- OCR engine abstraction.
- Tesseract adapter.
- OCR runner.
- OCR page object model.
- OCR cache integration.
- PDF page extraction support.

## v0.4 - Incremental build engine

### Added

- Dependency graph support.
- Dirty EDOM-node detection.
- Plugin dependency tracking.
- Plugin cache.
- General cached plugin execution.
- Hash cache and cache database support.

## v0.3 - Translation memory and TMX

### Added

- Translation memory model.
- Language-pair support.
- Hash-based lookup support.
- Reviewer metadata.
- TMX import and export.
- Robust XML handling for namespaces, comments, duplicate `tuv` elements, empty `seg` elements, and useful malformed XML errors.
- Unicode stress tests for emoji, supplementary planes, combining marks, right-to-left languages, mathematical alphabets, IPA, and CJK text.

## v0.2 - EDOM infrastructure

### Added

- EDOM node model.
- Tree traversal and walking.
- Node lookup by identifier.
- Heading hierarchy validation.
- Cross-reference validation foundations.
- JSON serialization and deserialization.
- Markdown-oriented import/export helpers.
- EDOM statistics.
- EDOM fingerprinting.

## v0.1 - Project scaffold

### Added

- Initial reusable toolkit scaffold for engineering books, workshop manuals, translated technical references, and specification documents.
- Build tooling baseline.
- Project initialization support.
- Initial tests and CI workflow.
