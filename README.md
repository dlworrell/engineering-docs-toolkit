# Engineering Docs Toolkit

Engineering Docs Toolkit (EDT) is a reusable publication and document-understanding engine for engineering books, workshop manuals, translated technical references, scientific notes, and specification documents.

The toolkit provides one common processing engine for projects such as HERKULES 1934, Atarix documentation, Catalyst specifications, and future technical translation projects. It is designed to preserve structure, semantics, accessibility, references, and translation memory instead of treating documents as flat text.

## Mission

EDT exists to turn complex technical documents into structured, accessible, reusable publications.

Its long-term goals are:

- Preserve technical meaning across format conversions.
- Support engineering-quality translation workflows.
- Preserve headings, captions, tables, figures, equations, references, and metadata.
- Make accessibility a first-class part of the build pipeline.
- Provide reusable tooling for downstream book and manual repositories.
- Support future mathematical knowledge extraction and solver integration.

## Processing model

```text
PDF / Markdown / source material
    -> OCR and page extraction
    -> layout analysis
    -> semantic recognition
    -> EDOM document tree
    -> translation memory
    -> semantic relationships and reference resolution
    -> accessibility metadata
    -> publishing outputs
```

## Current capabilities

- EDOM tree model with traversal, lookup, validation, serialization, metadata, and fingerprints.
- Translation memory with hash lookup, reviewer metadata, TMX import/export, Unicode stress handling, and robust XML behavior.
- Incremental build support with dependency graphs, dirty-node detection, plugin dependency tracking, and cached execution.
- OCR abstraction with page models, Tesseract integration, PDF page extraction, and OCR cache support.
- Accessibility pipeline with ARIA annotations, MathML support, figure alt text, table metadata, EPUB metadata, and accessibility reporting.
- Semantic recognition for headings, captions, tables, figures, equations, definitions, theorems, lemmas, corollaries, propositions, proofs, examples, exercises, algorithms, quotations, citations, titles, and authors.
- Mathematical metadata support for equation numbers, proof-end markers, Unicode mathematical glyphs, and semantic equation labels.
- Semantic relationships for theorem/proof links, figure/table captions, equation numbers, and cross-references.
- Reference indexing and resolution so textual references can resolve to semantic block identifiers.
- Semantic-to-EDOM metadata preservation, including resolved reference metadata.

## Project status

| Area | Status | Approx. completion |
| --- | --- | ---: |
| Core infrastructure | Stable | 95% |
| EDOM | Complete | 100% |
| Translation memory | Complete | 95% |
| Incremental build engine | Complete v1 | 90% |
| OCR framework | Complete v1 | 90% |
| Accessibility pipeline | Complete v1 | 90% |
| Semantic analysis | Mature | 95% |
| Semantic relationships and references | Mature | 95% |
| Publishing back ends | In progress | 50% |
| Advanced mathematical intelligence | Planned / early | 20% |
| Overall EDT | Active development | 75-80% |

The test suite is expected to remain green before merging changes. Recent development has kept the suite at roughly 180 passing tests.

## Roadmap

### Complete or substantially complete

1. EDOM infrastructure
2. Translation memory and TMX exchange
3. Incremental build engine
4. OCR abstraction
5. Accessibility pipeline
6. Semantic recognition
7. Semantic relationship and reference resolution

### Current focus

8. Semantic publishing
   - HTML anchors and links
   - EPUB navigation and landmarks
   - DOCX bookmarks and cross-references
   - PDF-oriented tagging and destinations

9. Advanced mathematics
   - Mathematical object model
   - Theorem numbering hierarchies
   - Proof nesting and proof trees
   - Assumptions, definitions, hypotheses, lemmas, and corollaries as first-class objects
   - Typed mathematical relationships
   - Mathematical dependency graphs
   - Structural theorem/proof validation hooks
   - Pluggable solver abstraction
   - Wolfram|Alpha adapter as one solver back end
   - Future SymPy, SageMath, Maxima, or similar adapters

## Downstream projects

EDT is the reusable engine. Book-specific repositories should hold project-specific source material, translation assets, outputs, and benchmark data.

For example, the HERKULES manual work belongs in the HERKULES repository, not inside EDT itself. EDT should provide the engine and reusable pipeline; the book repository should provide the source PDF, editorial structure, translations, review outputs, and project-specific reports.

## Development expectations

- Keep changes small and reviewable.
- Add tests for every new capability.
- Preserve semantic meaning before formatting.
- Keep Unicode and accessibility requirements in scope.
- Keep documentation synchronized with implementation.

Run the test suite with:

```bash
make test
```
