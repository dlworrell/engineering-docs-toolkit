# Reference Graph Architecture

The Reference Graph is EDT's directed relationship model for addressable document objects.

It is built from EDOM and records how semantic objects refer to one another. It supports validation, publishing, quality reporting, navigation, future semantic diffing, and knowledge-graph workflows.

## Purpose

Technical documents are not only trees. They contain cross-references, captions, equations, citations, theorem/proof relationships, definitions, examples, and other semantic links.

EDOM records the document hierarchy. The Reference Graph materializes the non-hierarchical relationships.

## Graph Model

The graph contains:

- Nodes: addressable EDOM objects.
- Edges: references from one object to another.
- Broken references: references whose targets do not exist.
- Orphans: addressable objects expected to be referenced but receiving no incoming references.

Conceptually:

```text
paragraph-12 -> figure-3.2
paragraph-19 -> theorem-4.1
proof-4.1    -> theorem-4.1
caption-8    -> figure-8
```

## Node Data

A graph node records:

- Node identifier
- Kind
- Page or source location when available
- Incoming references
- Outgoing references
- Broken references
- Orphan status

## Reference Sources

References are derived from EDOM metadata and semantic relationships. Common reference sources include:

- Cross-references in prose
- Figure references
- Table references
- Equation references
- Definition references
- Theorem, lemma, and corollary references
- Citation references
- Caption ownership
- Proof relationships

## Validation Integration

The validation subsystem uses reference information to detect:

- Broken references
- Orphaned addressable objects
- Circular references
- Self references

Validation reports detailed findings. The Reference Graph provides reusable relationship data for other subsystems.

## Publishing Integration

Publishers use reference graph data to generate stable anchors, hyperlinks, navigation structures, backlinks, indexes, and cross-reference displays.

Publishers should not rediscover references from rendered text. They should consume reference data produced upstream.

## Quality Report Integration

Quality reports summarize graph health through metrics such as:

- Total nodes
- Total edges
- Broken references
- Orphaned objects
- Reference completeness
- Publication readiness

## Future Direction

The Reference Graph is the foundation for future semantic document capabilities, including:

- Semantic diffing
- Knowledge graph export
- Citation network analysis
- Theorem dependency graphs
- Glossary relationship graphs
- Standards compliance mapping
- Living document comparison

The graph should remain deterministic and reproducible so that downstream reports and publications can be compared across builds.