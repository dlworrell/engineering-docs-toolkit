# SKOS

## Purpose

SKOS (Simple Knowledge Organization System) is a W3C standard for representing and linking knowledge organization systems such as thesauri, taxonomies, classification schemes, subject-heading systems, controlled vocabularies, and authority lists.

For EDT, SKOS provides a standards-based way to model controlled terminology, concept schemes, subject classification, multilingual labels, semantic relationships, and mappings between vocabularies.

## Current Standard

The normative SKOS specification is the W3C Recommendation published on 18 August 2009. It remains the current W3C Recommendation and defines the standard vocabulary, semantics, and integrity conditions.

EDT profiles using SKOS should record:

- The concept scheme identifier.
- The vocabulary release or snapshot.
- The language and notation policies.
- The mapping sources used.
- Any local extensions or constraints.
- The validation rules applied.

## Adoption Decision

EDT classifies SKOS as **Adopt** for controlled vocabularies and concept schemes, and **Bridge** for interchange with external taxonomies and knowledge-organization systems.

Rationale:

- SKOS is a mature W3C standard designed specifically for thesauri, taxonomies, classifications, and subject-heading systems.
- It supports multilingual labels, notes, hierarchical and associative relationships, collections, notations, and cross-scheme mappings.
- It is lightweight enough for practical document-engineering workflows.
- It complements rather than replaces EDOM, RDF, OWL, and profile-specific validation.

## Core Concepts

Representative SKOS constructs include:

| SKOS construct | Purpose |
| --- | --- |
| `skos:Concept` | A unit of thought or meaning within a knowledge organization system |
| `skos:ConceptScheme` | A vocabulary, thesaurus, taxonomy, or classification scheme |
| `skos:prefLabel` | Preferred human-readable label in a language |
| `skos:altLabel` | Alternative or synonymous label |
| `skos:hiddenLabel` | Search or matching label not normally displayed |
| `skos:notation` | Formal code or classification notation |
| `skos:broader` | Direct broader concept relationship |
| `skos:narrower` | Direct narrower concept relationship |
| `skos:related` | Associative concept relationship |
| `skos:definition` | Formal or explanatory definition |
| `skos:scopeNote` | Guidance on intended meaning or use |
| `skos:example` | Example of concept use |
| `skos:historyNote` | Historical information |
| `skos:changeNote` | Change history |
| `skos:editorialNote` | Internal editorial information |
| `skos:Collection` | Group of concepts assembled for a purpose |
| `skos:OrderedCollection` | Ordered group of concepts |
| `skos:exactMatch` | Strong cross-scheme equivalence mapping |
| `skos:closeMatch` | Close but not necessarily exact mapping |
| `skos:broadMatch` | Broader mapping across schemes |
| `skos:narrowMatch` | Narrower mapping across schemes |
| `skos:relatedMatch` | Associative mapping across schemes |

## Where EDT Uses SKOS

- Controlled terminology for engineering and publishing profiles.
- Subject classification and indexing.
- Glossary and taxonomy management.
- Normalization of variant terms.
- Multilingual labels and terminology mappings.
- Mapping imported subject vocabularies into a project vocabulary.
- Classification of semantic document objects.
- Search, navigation, faceting, and discovery.
- Validation of allowed terms and concept identifiers.
- Export to RDF-based metadata and knowledge-graph systems.

## Where EDT Does Not Use SKOS

SKOS is not EDT's canonical semantic document model. It does not represent document hierarchy, prose, equations, figures, tables, source regions, validation findings, publication layout, or transformation provenance.

SKOS also is not a substitute for a formal domain ontology when stronger logical constraints or machine reasoning are required. OWL or another formal knowledge-representation language may be appropriate for those cases.

The boundary is:

```text
EDOM owns document semantics and structure.
SKOS owns controlled concepts, labels, taxonomy relationships, and vocabulary mappings.
```

## Mapping to EDT and EDOM

Representative mappings are:

| EDT / EDOM concept | SKOS mapping |
| --- | --- |
| Controlled subject | `skos:Concept` |
| Vocabulary or taxonomy | `skos:ConceptScheme` |
| Display term | `skos:prefLabel` |
| Synonym or variant term | `skos:altLabel` |
| Search-only synonym or misspelling | `skos:hiddenLabel` |
| Classification code | `skos:notation` |
| Parent category | `skos:broader` |
| Child category | `skos:narrower` |
| Associated concept | `skos:related` |
| Definition | `skos:definition` |
| Usage guidance | `skos:scopeNote` |
| Example | `skos:example` |
| Historical context | `skos:historyNote` |
| Vocabulary revision note | `skos:changeNote` |
| Imported equivalent concept | SKOS mapping property |
| EDOM node classification | Reference from node metadata to a concept URI |

EDOM should store concept identifiers as stable references rather than copying only labels. Labels may change while the concept identifier remains stable.

## Concept Identity

A SKOS concept should have a stable URI or another stable identifier mapped to a URI in the exported graph.

EDT should distinguish clearly between:

- The concept itself.
- A label used to name the concept.
- A notation used to classify the concept.
- A document node tagged with the concept.
- A mapping assertion connecting the concept to another scheme.

Two concepts must not be merged merely because they share a label. Conversely, two labels may refer to the same concept.

## Labels and Languages

SKOS labeling is especially useful for multilingual and terminology-rich documents.

An EDT SKOS profile may define:

- The required preferred-label languages.
- Whether one preferred label per language is required.
- Allowed alternative-label sources.
- Hidden-label rules for search and normalization.
- Language-tag policy.
- Capitalization and punctuation conventions.
- Acronym and abbreviation treatment.
- Transliteration policy.

EDT should preserve language tags and should not collapse multilingual labels into one untyped string.

## Hierarchical Relationships

SKOS distinguishes direct hierarchical relationships from transitive closure.

EDT should treat:

- `skos:broader` and `skos:narrower` as asserted direct relationships.
- `skos:broaderTransitive` and `skos:narrowerTransitive` as transitive super-properties used for inference or query.

A profile must not assume that every asserted hierarchy is a strict tree. Taxonomies may contain polyhierarchy, and concepts may have multiple broader concepts.

Cycles should be detected and handled according to profile policy. Some graphs may be syntactically valid RDF while still violating the intended taxonomy design.

## Associative Relationships

`skos:related` represents an associative semantic relationship that is neither broader nor narrower.

EDT should not use `skos:related` as an unspecified catch-all for every relationship. Profiles should define when associative links are appropriate and should prefer more specific domain properties when the relationship has important operational meaning.

## Collections

SKOS collections group concepts without asserting that the collection itself is a concept in the hierarchy.

EDT may use collections for:

- Curated subsets.
- Navigation groups.
- Publication-specific term sets.
- Facets assembled from concepts in different branches.
- Ordered lists such as process stages or display sequences.

A collection should not be substituted for a concept merely because it has a label.

## Mapping Between Schemes

SKOS mapping properties support cross-vocabulary alignment.

EDT should preserve the distinction among:

- Exact equivalence.
- Close equivalence.
- Broader mapping.
- Narrower mapping.
- Related mapping.

Mapping assertions should record provenance, including:

- Source and target schemes.
- Scheme versions.
- Mapping method.
- Responsible agent.
- Review status.
- Date of assertion.
- Evidence or rationale where available.

EDT must not promote `skos:closeMatch` to `skos:exactMatch` automatically.

## Import Strategy

A SKOS importer should preserve:

- Concept and scheme identifiers.
- Preferred, alternative, and hidden labels.
- Language tags.
- Notations and datatypes.
- Documentation notes.
- Hierarchical and associative relationships.
- Collections and ordering.
- Cross-scheme mappings.
- Source graph, retrieval time, and vocabulary version.
- RDF serialization and named-graph context where relevant.

Unknown extension properties should be retained as typed RDF assertions or extension metadata rather than discarded.

Imported concepts should not silently overwrite locally curated concepts. Conflicts should be reported and resolved through declared profile policy.

## Export Strategy

A SKOS exporter should:

1. Select a declared concept scheme and vocabulary snapshot.
2. Generate stable concept URIs.
3. Export labels with language tags.
4. Export notations with explicit datatypes where appropriate.
5. Export direct hierarchical and associative relationships.
6. Export notes and definitions.
7. Export collections and ordering.
8. Export cross-scheme mappings with provenance links where supported.
9. Validate the graph against SKOS integrity conditions and project rules.
10. Preserve the generated RDF and validation output as build artifacts.

Possible serializations include Turtle, RDF/XML, JSON-LD, N-Triples, or another RDF syntax selected by the publication or repository profile.

## Validation

EDT validation may include:

- Missing concept identifiers.
- Duplicate identifiers.
- Missing concept-scheme membership.
- Multiple preferred labels in the same language where prohibited.
- The same literal used simultaneously as preferred, alternative, or hidden label in a way that violates SKOS integrity conditions.
- Broken broader, narrower, related, or mapping targets.
- Hierarchical cycles forbidden by the project profile.
- Concepts unreachable from a declared top concept.
- Invalid or duplicate notations.
- Mapping assertions lacking source or target scheme provenance.
- `skos:related` conflicts with hierarchical relationships.
- Use of undeclared language tags or notation datatypes.
- Concepts referenced by EDOM nodes but absent from the selected vocabulary snapshot.

Schema or RDF syntax validity alone is insufficient. A graph may be valid RDF while still violating SKOS integrity conditions or project-specific taxonomy rules.

## Relationship to RDF and OWL

SKOS is defined using RDF and can be combined with OWL.

EDT should use SKOS when the main requirement is to publish and connect practical vocabularies. OWL should be considered when the project requires stronger formal semantics, class restrictions, property axioms, or automated reasoning beyond the SKOS model.

A SKOS concept is not automatically equivalent to an OWL class. Profiles must define any explicit bridge between taxonomy concepts and ontology classes.

## Relationship to Dublin Core

Dublin Core describes resources; SKOS describes controlled concepts and concept schemes.

A document may use Dublin Core for descriptive metadata such as title, creator, language, and subject, while the subject value points to a SKOS concept URI.

Example boundary:

```text
Dublin Core states that a document has a subject.
SKOS defines the subject concept and its relationships.
```

## Relationship to Glossaries

An EDT glossary may overlap with a SKOS concept scheme, but the two are not necessarily identical.

A glossary entry may include:

- A document-facing definition.
- Usage examples.
- Domain-specific notes.
- Abbreviations.
- Cross-references.
- Publication placement.

A SKOS concept may provide the stable concept identity, labels, mappings, and taxonomy relationships. Profiles may link glossary entries to SKOS concepts rather than forcing all glossary content into the SKOS graph.

## Profiles

An EDT SKOS profile may specify:

- Concept-scheme identifier and version.
- Required languages.
- Label cardinality rules.
- Allowed notation systems.
- Required top concepts.
- Allowed hierarchy depth.
- Cycle policy.
- Polyhierarchy policy.
- Required definitions or scope notes.
- Mapping policy.
- External vocabulary dependencies.
- Serialization format.
- Validation rules and tooling.
- Governance and review workflow.

## Governance and Change Control

Controlled vocabularies evolve. EDT should treat vocabulary changes as governed semantic changes rather than ordinary text edits.

A change process should record:

- Added, modified, deprecated, split, merged, or removed concepts.
- Identifier continuity.
- Label changes.
- Relationship changes.
- Mapping changes.
- Migration guidance for documents using affected concepts.
- Responsible reviewers.
- Release date and version.

Deprecated concepts should remain resolvable where possible and should point to replacement or successor concepts through declared project policy.

## Provenance

Each imported, generated, or curated assertion should be traceable to its source.

Relevant provenance includes:

- Vocabulary release.
- Source file or endpoint.
- Retrieval time.
- Curator or automated process.
- Mapping tool and version.
- Human review state.
- Transformation rules.
- Validation results.

EDT's W3C PROV support may be used to describe these activities and derivations in greater detail.

## Design Notes

SKOS gives EDT a practical, interoperable foundation for terminology and classification without forcing every vocabulary into a heavyweight ontology.

The architectural boundary is:

```text
EDOM owns document semantics and references.
SKOS owns controlled concepts, labels, schemes, and taxonomy mappings.
RDF carries the graph representation.
OWL may add stronger formal semantics when required.
```

## References

- W3C, *SKOS Simple Knowledge Organization System Reference*: https://www.w3.org/TR/skos-reference/
- W3C, *SKOS Simple Knowledge Organization System Primer*: https://www.w3.org/TR/skos-primer/
