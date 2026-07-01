# Engineering Documents Toolkit (EDT)

**A Semantic Document Engineering Platform**

EDT imports, understands, validates, transforms, translates, and publishes complex technical documents while preserving provenance.

EDT is not just a format converter. It treats documents as semantic knowledge structures rather than flat text or page images. Source material is normalized into the Engineering Document Object Model (EDOM), validated for structural and semantic integrity, enriched with references and metadata, and published into reproducible output formats.

## Why EDT Exists

Technical knowledge often outlives the software, file formats, and page layouts used to create it. EDT exists to preserve that knowledge independently of presentation.

The project charter defines the mission, scope, principles, and relationship to the broader Catalyst ecosystem: [PROJECT_CHARTER.md](PROJECT_CHARTER.md).

## Current Release Target

**Target:** EDT 1.0.0  
**Current phase:** Documentation Synchronization  
**Core engineering status:** Feature-complete for the 1.0 validation and publishing foundation

## Implemented Capabilities

### Import and Recognition

- PDF-oriented import pipeline
- OCR abstraction and Tesseract integration
- Page extraction and OCR caching
- Layout analysis for headings, paragraphs, tables, figures, equations, notes, and columns
- Semantic recognition for technical and mathematical document structures

### Canonical Document Model

- Engineering Document Object Model (EDOM)
- Tree traversal, lookup, validation, serialization, metadata, and fingerprints
- Semantic-to-EDOM metadata preservation
- Equation numbers, proof markers, captions, references, and accessibility metadata

### Validation and Quality

- Structural validation
- Semantic validation
- Caption validation
- Reference validation
- Orphaned reference detection
- Reference graph generation
- Quality report generation

### Publishing and Translation

- HTML export
- Markdown export
- EPUB export
- Translation memory support
- TMX import/export
- Unicode stress handling for translation workflows

### Build and Accessibility

- Incremental build support
- Dependency graph tracking
- Dirty-node detection
- Plugin dependency tracking
- Accessibility metadata
- ARIA annotations
- MathML support
- Figure alt text and table accessibility support

## Processing Model

```text
Source documents
    -> import
    -> OCR / extraction
    -> layout analysis
    -> semantic recognition
    -> EDOM
    -> validation
    -> reference graph
    -> quality reports
    -> publishing outputs
```

## Catalyst Ecosystem Role

Within the Catalyst ecosystem:

- **AES** defines engineering doctrine.
- **AEMS** evaluates engineering compliance.
- **EDT** provides semantic document engineering.
- **HERKULES** serves as the flagship demonstration and regression corpus.

EDT is the reusable document engine. Book-specific repositories should hold source material, editorial structure, translation assets, generated outputs, and project-specific reports.

## Project Status

| Area | Status |
| --- | --- |
| Core infrastructure | Stable |
| EDOM | Complete for 1.0 |
| OCR framework | Complete v1 |
| Layout analysis | Complete v1 |
| Semantic recognition | Mature |
| Validation | Frozen for 1.0 except bug fixes |
| Reference graph | Complete v1 |
| Quality reports | Complete v1 |
| HTML export | Complete v1 |
| Markdown export | Complete v1 |
| EPUB export | Complete v1 |
| Translation memory / TMX | Complete v1 |
| Documentation | In progress |
| Profile-driven semantics | Planned for post-1.0 |
| Advanced mathematical intelligence | Planned for post-1.0 |

## Getting Started

Run the test suite with:

```bash
make test
```

Install the package in editable mode with:

```bash
python -m pip install -e .
```

Then use the EDT CLI from the repository root or an EDT project workspace.

## Development Expectations

- Keep changes small and reviewable.
- Add tests for every new capability.
- Preserve semantic meaning before formatting.
- Keep Unicode, accessibility, provenance, and validation requirements in scope.
- Keep documentation synchronized with implementation.

## Documentation Roadmap

The next documentation work will add:

- Architecture handbook
- User guide
- Developer guide
- Standards survey
- EDOM specification
- Validation specification
- Reference graph specification
- Quality report specification
- First real book workflow
