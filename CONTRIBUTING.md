# Contributing to Engineering Docs Toolkit

Engineering Docs Toolkit (EDT) is a semantic document-processing toolkit. Contributions should improve document meaning, accessibility, translation quality, reproducibility, or publishing correctness.

## Engineering principles

1. Semantic correctness comes before visual formatting.
2. Accessibility is required, not optional.
3. Unicode and multilingual text must be preserved.
4. Tests are required for new behavior.
5. Build behavior should be deterministic.
6. Incremental processing and cache compatibility should be preserved.
7. Documentation should change with the implementation.
8. Small commits are preferred over broad rewrites.

## Commit discipline

Use small, logical commits.

Good examples:

- `Add equation number relationships`
- `Test reference resolver behavior`
- `Preserve semantic metadata in EDOM`

Avoid mixing unrelated changes. A code change, its focused tests, and its immediately relevant documentation may be grouped when they form one coherent change.

## Branch workflow

For larger changes:

1. Create a work branch from `main`.
2. Make small incremental commits.
3. Keep the branch passing tests.
4. Merge or fast-forward back to `main` only after the work is complete and reviewed.

## Testing

Run the test suite before merging:

```bash
make test
```

New features should include tests. Bug fixes should include regression tests when practical.

Current test coverage includes these major areas:

- EDOM
- serialization and traversal
- translation memory and TMX
- Unicode stress handling
- OCR and PDF page extraction
- accessibility metadata
- layout recognition
- semantic recognition
- semantic relationships
- reference resolution
- semantic-to-EDOM conversion
- incremental build and plugin cache behavior

## Coding style

- Use clear module boundaries.
- Prefer small focused functions.
- Use type hints.
- Use dataclasses for structured value objects when appropriate.
- Keep deterministic behavior where possible.
- Avoid hidden global state.
- Do not silently discard metadata.
- Do not flatten semantic structure merely to match an output format.

## Accessibility requirements

When adding or changing document processing behavior, consider:

- ARIA annotations
- MathML preservation or generation
- figure alt text
- table captions and header metadata
- EPUB accessibility metadata
- semantic roles
- reading order
- Unicode preservation

A feature that improves visual output while degrading accessibility is a regression unless explicitly justified and documented.

## Translation requirements

Translation-related work should preserve:

- source text
- target text
- language pair
- stable hashes
- reviewer metadata
- terminology consistency
- TMX import/export compatibility
- Unicode text and combining marks

Terminology locking and glossary enforcement are expected future capabilities.

## Semantic relationship requirements

When adding new semantic entities or relationships, consider whether they should affect:

- EDOM metadata
- reference resolution
- accessibility labels
- publishing links
- incremental dependency tracking
- future document graph queries

Relationship names should be explicit and stable, such as `has_proof`, `has_caption`, `has_number`, or `references`.

## Mathematical intelligence requirements

Advanced mathematical work should begin with representation before automation.

Preferred order:

1. mathematical object model
2. numbering hierarchy
3. typed relationships
4. proof tree representation
5. dependency graph
6. structural validation hooks
7. solver abstraction
8. solver adapters

Solver integrations should use a generic `SolverEngine` interface rather than coupling EDT directly to one vendor or service.

## Downstream project boundaries

EDT is the reusable engine. Project-specific material belongs in downstream repositories.

For example, HERKULES book assets should live in the HERKULES repository, including:

- source manual PDF
- OCR snapshots
- translation drafts
- project glossary
- generated outputs
- book-specific reports
- benchmark expectations

EDT may include reusable examples and fixtures, but it should not become the canonical storage location for downstream book projects.

## Pull request checklist

Before merging, confirm:

- [ ] The change has a clear purpose.
- [ ] Commits are small and logical.
- [ ] Tests were added or updated.
- [ ] `make test` passes.
- [ ] Documentation was updated if behavior changed.
- [ ] Accessibility impact was considered.
- [ ] Unicode and translation behavior were not regressed.
- [ ] Semantic metadata is preserved where applicable.
