# Engineering Docs Toolkit Project Plan

## Purpose

Engineering Docs Toolkit (EDT) is a reusable engine for technical document processing, translation, accessibility, and publication. It is intended to serve downstream repositories that contain specific manuals, books, specifications, or translation projects.

EDT should remain the reusable toolkit. Book-specific artifacts, source PDFs, editorial drafts, translation output, and benchmark corpora should live in their own repositories.

## Core design principles

1. Preserve semantic meaning before visual formatting.
2. Treat accessibility as a required output, not a later cleanup step.
3. Preserve Unicode, mathematical notation, and multilingual text without lossy normalization.
4. Keep document structure explicit and testable.
5. Make all major transformations incremental and cacheable.
6. Keep translation memory reusable across projects.
7. Keep downstream projects separate from reusable toolkit code.
8. Require tests for new behavior.

## Architecture

```text
Source material
    PDF / Markdown / structured text
        |
        v
OCR and page extraction
        |
        v
Layout model
        |
        v
Semantic recognition
        |
        v
Semantic document and relationship graph
        |
        v
EDOM
        |
        +--> Translation memory
        +--> Accessibility metadata
        +--> Reference resolution
        +--> Incremental build cache
        |
        v
Publishing outputs
    HTML / EPUB / DOCX / PDF-oriented output
```

## Subsystems

### EDOM

EDOM is the core editable document object model. It provides structured nodes, child traversal, lookup, validation, serialization, metadata, and deterministic fingerprints for incremental processing.

Status: complete.

### Translation memory

The translation memory subsystem supports reusable translation units, language pairs, hash-based lookups, reviewer metadata, and TMX import/export. It includes robust XML handling and Unicode stress coverage.

Status: complete / mature.

### Incremental build engine

The incremental build subsystem tracks document dependencies, dirty nodes, plugin dependencies, and cached execution. It is intended to keep large technical documents rebuildable without reprocessing every node.

Status: complete v1.

### OCR framework

The OCR subsystem provides an engine interface, Tesseract adapter, page model, PDF page extraction, and OCR cache integration.

Status: complete v1.

### Accessibility pipeline

The accessibility subsystem includes ARIA annotations, MathML, figure alt-text support, table metadata, EPUB accessibility metadata, and accessibility reporting.

Status: complete v1.

### Semantic layer

The semantic layer recognizes document meaning beyond layout. It supports headings, captions, figures, tables, equations, theorem-like blocks, proofs, examples, algorithms, quotations, citations, bibliography, index material, titles, and authors.

Status: mature.

### Semantic relationships

The relationship layer connects semantic objects. It supports theorem/proof relationships, figure/table captions, equation numbers, cross-reference detection, reference indexing, reference resolution, and resolved reference export to EDOM metadata.

Status: mature.

### Publishing back ends

Publishing back ends are the next major development area. EDT has the semantic and EDOM infrastructure needed for high-quality exports, but HTML, EPUB, DOCX, and PDF-oriented publishing should now consume semantic references and metadata more directly.

Status: in progress.

### Advanced mathematical intelligence

The advanced math layer is planned as a major future direction. The current system recognizes equations and mathematical metadata; the next stage is to represent mathematical objects, proof structure, typed relationships, dependency graphs, validation hooks, and solver integrations.

Status: planned / early.

## Current completion estimates

| Area | Approx. completion |
| --- | ---: |
| Core infrastructure | 95% |
| EDOM | 100% |
| Translation pipeline | 95% |
| Incremental build engine | 90% |
| OCR framework | 90% |
| Accessibility pipeline | 90% |
| Semantic analysis | 95% |
| Semantic relationships and references | 95% |
| Publishing back ends | 50% |
| Advanced mathematical intelligence | 20% |
| Overall EDT | 75-80% |

These estimates describe engineering maturity, not a promise that every edge case has been implemented.

## Roadmap

### Phase 1 - EDOM infrastructure

Status: complete.

Completed capabilities:

- `walk()` style traversal
- node lookup by identifier
- heading hierarchy validation
- cross-reference validation foundations
- JSON serialization and deserialization
- metadata preservation
- fingerprinting

### Phase 2 - Translation memory

Status: complete / mature.

Completed capabilities:

- language pairs
- hash-based lookups
- TMX import/export
- reviewer metadata
- robust XML handling
- Unicode stress testing

### Phase 3 - Incremental build engine

Status: complete v1.

Completed capabilities:

- dependency graph
- dirty-node detection
- plugin dependency tracking
- cached plugin execution

### Phase 4 - OCR abstraction

Status: complete v1.

Completed capabilities:

- OCR engine interface
- Tesseract adapter
- page object model
- PDF page extraction
- OCR cache integration

### Phase 5 - Accessibility pipeline

Status: complete v1.

Completed capabilities:

- MathML generation
- ARIA annotations
- figure alt-text support
- table accessibility metadata
- EPUB accessibility metadata
- accessibility reports

### Phase 6 - Semantic publishing

Status: in progress.

Planned capabilities:

- HTML anchors from semantic block IDs
- HTML hyperlinks from resolved references
- EPUB landmarks and navigation documents
- EPUB internal hyperlinks
- DOCX bookmarks and cross-reference fields
- PDF-oriented tags, destinations, and link annotations

### Phase 7 - Citation engine

Status: planned.

Planned capabilities:

- structured citations such as `[17]`, author-year forms, DOI, ISBN, RFC, ISO, and BibTeX-style references
- bibliography entry recognition
- citation-to-bibliography relationship graph
- citation export for HTML, EPUB, DOCX, and PDF

### Phase 8 - Document graph

Status: planned.

Planned capabilities:

- explicit graph abstraction over semantic nodes and relationships
- incoming and outgoing reference queries
- path search
- reverse reference lookup
- dependency lookup
- graph export and visualization support

### Phase 9 - Advanced mathematics

Status: planned / early.

Planned capabilities:

- mathematical object model
- theorem numbering hierarchies
- proof nesting and proof trees
- assumptions, hypotheses, definitions, lemmas, propositions, corollaries, and conjectures as first-class objects
- references between mathematical objects
- typed mathematical relationships such as `uses_definition`, `uses_equation`, `uses_theorem`, `extends`, `generalizes`, `specializes`, `proves`, and `assumes`
- mathematical dependency graphs
- theorem/proof validation hooks
- pluggable `SolverEngine` abstraction
- Wolfram|Alpha adapter as one solver backend
- future SymPy, SageMath, Maxima, or similar adapters
- optional automatic solutions, derivations, and step explanations when requested

## Downstream project policy

EDT should not become a storage location for individual book projects. For example, HERKULES-specific assets should live in the HERKULES repository. EDT should provide reusable code, documentation, tests, and examples.

A downstream book repository may contain:

- source PDFs
- scanned images
- OCR outputs
- EDOM snapshots
- translation memory files
- glossary locks
- editorial review notes
- generated reports
- HTML, EPUB, DOCX, or PDF outputs
- project-specific benchmark expectations

## Current priority

The next high-value milestone is semantic publishing: using resolved semantic references and EDOM metadata to produce real links, anchors, landmarks, bookmarks, and accessibility-aware publication outputs.

In parallel, Phase 9 should begin with a mathematical object model and numbering hierarchy so future mathematical intelligence has a stable representation to build on.
