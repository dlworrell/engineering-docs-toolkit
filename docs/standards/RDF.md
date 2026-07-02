# RDF

## Purpose

The Resource Description Framework (RDF) is a W3C graph data model for representing information about resources and relationships among them. RDF expresses statements as subject-predicate-object triples and organizes those statements into graphs and datasets.

For EDT, RDF is the common graph foundation for interoperable metadata, provenance, controlled vocabularies, linked identifiers, and knowledge-graph exports.

## Current Standard

RDF 1.1 remains the latest W3C Recommendation.

RDF 1.2 is in the W3C Candidate Recommendation stage. The 7 April 2026 Candidate Recommendation Snapshot introduces, among other changes:

- Triple terms and a revised reification model.
- Directional language-tagged strings.
- A mechanism for announcing the RDF version used by a data representation.

EDT should therefore:

- **Adopt RDF 1.1** for production interchange.
- **Evaluate RDF 1.2** and design for forward compatibility.
- Require profiles to declare the RDF version and serialization used.
- Avoid emitting RDF 1.2-only features into an RDF 1.1 target.

## Adoption Decision

EDT classifies RDF as **Adopt** for graph interchange and **Bridge** for external linked-data systems.

Rationale:

- RDF is the shared foundation for W3C PROV, SKOS, many Dublin Core representations, Schema.org JSON-LD, and OWL.
- It supports globally identified entities and relationships across independently managed vocabularies.
- It provides a standard graph representation without forcing RDF to become EDT's internal document tree.
- It allows EDT metadata and reference relationships to participate in broader knowledge graphs.

## Core Model

An RDF triple contains:

| Position | Meaning |
| --- | --- |
| Subject | The resource being described |
| Predicate | The relationship or property being asserted |
| Object | Another resource or a literal value |

A set of triples forms an RDF graph. An RDF dataset contains one default graph and zero or more named graphs.

Representative Turtle:

```turtle
@prefix schema: <https://schema.org/> .
@prefix prov: <http://www.w3.org/ns/prov#> .

<https://example.org/document/42>
    a schema:TechArticle ;
    schema:name "System Architecture" ;
    prov:wasDerivedFrom <https://example.org/source/42.pdf> .
```

The prefixes are serialization conveniences. The complete IRIs identify the vocabulary terms.

## Where EDT Uses RDF

- W3C PROV export.
- SKOS concept schemes and terminology mappings.
- Schema.org and JSON-LD publication metadata.
- Dublin Core metadata exchange.
- Linked identifiers for documents, contributors, organizations, concepts, sources, and publications.
- Reference-graph and relationship export.
- Named graphs for separating assertions by source, profile, or provenance context.
- Interchange with repositories, triple stores, and knowledge graphs.

## Where EDT Does Not Use RDF

RDF is not EDT's canonical semantic document representation. EDOM remains authoritative for ordered document hierarchy, semantic nodes, source regions, validation state, publication profiles, and transformation behavior.

RDF graphs are sets of statements and do not inherently preserve:

- Child order.
- Document sequence.
- Contiguous text spans.
- Page geometry.
- Source-region coordinates.
- Publication layout.
- Profile-specific processing rules.

These properties can be modeled in RDF, but doing so does not make RDF a better replacement for EDOM's purpose-built document model.

The architectural boundary is:

```text
EDOM owns document structure and semantic processing.
RDF carries selected entities, metadata, and relationships into graph ecosystems.
```

## Mapping to EDT

Representative mappings are:

| EDT concept | RDF representation |
| --- | --- |
| Document | IRI-identified resource |
| EDOM node | IRI or blank node when exported |
| Stable identifier | IRI or typed literal |
| Metadata field | Predicate-object assertion |
| Reference-graph edge | RDF triple or qualified relationship node |
| External identity | IRI link |
| Contributor | Agent resource |
| Source file | Entity resource |
| Import or publication operation | Activity resource, usually through W3C PROV |
| Controlled subject | SKOS concept IRI |
| Vocabulary | RDF namespace and ontology or concept scheme |
| Profile or dataset boundary | Named graph or dataset metadata |

Not every EDOM node requires a public IRI. Profiles should define which entities receive stable identifiers and which may remain local.

## IRI Policy

EDT RDF exports should use stable, absolute IRIs for entities intended to be referenced outside the package.

A profile should define:

- Base IRI.
- Identifier construction rules.
- Persistence expectations.
- Canonical document and publication IRIs.
- Version and edition identifiers.
- Whether fragment identifiers identify document parts.
- How local identifiers map to external IRIs.

An IRI should not be reassigned to a different referent. Renaming a label or moving a resource does not justify silently changing its identity.

## Literals

RDF literals may carry datatypes or language tags.

EDT should preserve:

- Numeric, boolean, date, time, and other typed values.
- Language-tagged strings.
- Lexical values needed for round-trip or audit.
- Direction metadata when targeting RDF 1.2 and the selected serialization supports it.

Plain strings should not be used where a well-defined datatype or identified resource is required by the profile.

## Blank Nodes

Blank nodes identify local existential resources without globally stable names.

EDT may use blank nodes for short-lived structural groupings or serialization convenience, but should prefer IRIs when:

- The entity must be referenced from another file or graph.
- Provenance must survive export and re-import.
- The entity participates in long-lived identity or reconciliation.
- Stable diffing and reproducibility matter.

Blank-node identifiers are not stable public identifiers and must not be treated as such.

## Named Graphs and Datasets

Named graphs can preserve useful boundaries among groups of assertions.

EDT may use them to separate:

- Source-imported assertions.
- EDT-generated assertions.
- Human-curated assertions.
- Profile-derived metadata.
- External registry data.
- Publication-specific projections.
- Historical snapshots.

A graph name does not, by itself, state who asserted the graph or when. Provenance relationships must be modeled explicitly, for example with W3C PROV.

## Serialization Strategy

EDT may support multiple RDF syntaxes while preserving one graph model.

Likely serializations include:

| Serialization | EDT use |
| --- | --- |
| Turtle | Human-readable source and test fixtures |
| JSON-LD | Web publication and Schema.org metadata |
| N-Triples | Simple line-oriented exchange |
| N-Quads | Dataset and named-graph exchange |
| TriG | Human-readable datasets and named graphs |
| RDF/XML | Compatibility with XML-oriented repositories |

Profiles must declare the serialization, media type, RDF version, base IRI behavior, and canonicalization requirements.

Equivalent RDF graphs can have very different byte serializations. Byte comparison alone is therefore not a reliable graph-equivalence test.

## Canonicalization and Fixity

RDF graph equality is not the same as file-byte equality, especially when blank nodes are present.

EDT preservation workflows should distinguish:

- Fixity of the serialized RDF file.
- Semantic equivalence of parsed RDF graphs.
- Dataset equivalence including named graphs.
- Canonicalized graph or dataset digests, when a declared canonicalization method is used.

The canonicalization algorithm and version must be recorded. EDT must not claim a semantic digest without specifying the method used to produce it.

## Import Strategy

An RDF importer should preserve:

- RDF version where declared or inferable.
- Source serialization and media type.
- Base IRI and prefix declarations.
- Default and named graph boundaries.
- IRIs, blank nodes, literals, datatypes, and language tags.
- Vocabulary terms not understood by EDT.
- Retrieval source, time, and content fixity.
- Parser warnings and unsupported features.

Imported assertions should be mapped into EDOM only when a profile defines the mapping. Unknown graph data should remain available as RDF extension data rather than being discarded.

External RDF must not silently overwrite curated EDOM metadata. Conflicting assertions should retain their source and be reported for resolution.

## Export Strategy

An RDF exporter should:

1. Select a declared RDF version and profile.
2. Assign stable IRIs according to policy.
3. Map validated EDOM entities and relationships to declared vocabularies.
4. Preserve language and datatype information.
5. Separate assertion sets into named graphs where required.
6. Emit the selected serialization deterministically where practical.
7. Validate syntax and profile constraints.
8. Preserve the generated graph, configuration, and validation results as build artifacts.

Exporters should report EDOM semantics that lack an RDF mapping rather than implying full-model equivalence.

## RDF 1.2 Readiness

EDT should prepare for RDF 1.2 without making Candidate Recommendation features mandatory for production workflows.

### Triple terms and reification

RDF 1.2 permits an RDF triple to appear as a triple term in the object position of another triple and defines a revised reification mechanism using `rdf:reifies`.

This is relevant to EDT because provenance and confidence may apply to individual assertions. However, production RDF 1.1 exports should continue using RDF 1.1-compatible qualification patterns until a profile explicitly targets RDF 1.2.

### Directional language-tagged strings

RDF 1.2 adds base-direction information to language-tagged strings. EDT's semantic text model should preserve language and direction independently so either RDF 1.1-compatible or RDF 1.2-native output can be generated.

### Version declaration

RDF 1.2 introduces a way to announce which RDF version is used. EDT exporters targeting RDF 1.2 should emit version information as required by the selected syntax and profile.

## Validation

EDT RDF validation may include:

- Syntax errors.
- Relative IRIs where absolute IRIs are required.
- Reused IRIs with conflicting intended identity.
- Invalid datatype lexical forms.
- Missing or malformed language tags.
- Broken references to required local resources.
- Use of vocabulary terms outside the declared profile.
- RDF 1.2-only terms or syntax in an RDF 1.1 target.
- Missing named-graph provenance.
- Blank nodes used where persistent identity is required.
- Unsupported entailment assumptions.
- Violations of SHACL, ShEx, or profile-specific constraints.
- Differences between expected and generated graphs.

RDF syntax validity proves only that the graph can be parsed. It does not prove that the metadata is complete, internally consistent, or compliant with a domain profile.

## Entailment

RDF, RDF Schema, and OWL define different levels of semantic entailment.

EDT profiles must state whether validation and query operate on:

- Explicit triples only.
- RDF entailment.
- RDF Schema entailment.
- OWL entailment.
- A custom rule set.

A system must not assume that inferred triples were explicitly asserted. When provenance matters, EDT should distinguish asserted, imported, generated, and inferred statements.

## Relationship to RDF Schema

RDF Schema provides basic vocabulary-definition features such as classes, properties, domains, ranges, and subclass relationships.

EDT may use RDFS to document lightweight vocabularies, but RDFS domain and range statements have entailment semantics and are not merely input-validation rules.

Constraint validation should use an explicit validation language or EDT profile rules rather than relying on RDFS alone.

## Relationship to OWL

OWL adds stronger ontology semantics and reasoning capabilities.

EDT should use OWL only when the project requires formal class expressions, property axioms, identity reasoning, or other ontology behavior beyond RDF and RDFS.

Not every taxonomy or document profile needs an ontology. SKOS and profile validation are often the more practical choice.

## Relationship to JSON-LD

JSON-LD is an RDF serialization and linked-data processing model that integrates naturally with JSON and web publishing.

EDT's Schema.org output should normally use JSON-LD, while preserving the distinction between:

- The JSON-LD document bytes.
- The expanded RDF graph.
- The source EDOM data.
- The context used to interpret compact terms.

Changing a JSON-LD context can change the interpreted RDF graph even when the compact JSON appears similar. Contexts are therefore versioned dependencies and part of publication provenance.

## Profiles

An EDT RDF profile may specify:

- RDF version.
- Required vocabularies and versions.
- Base IRI and identifier policy.
- Required entity types and properties.
- Serialization and media type.
- Named-graph policy.
- Blank-node restrictions.
- Language and datatype rules.
- Entailment regime.
- Constraint language and shapes.
- Canonicalization method.
- External context and vocabulary dependencies.
- Validation tools and expected graph fixtures.

## Provenance

Every imported, generated, inferred, or curated RDF assertion should be attributable to a source or process when that distinction matters.

EDT may use W3C PROV to record:

- Source graphs and files.
- Import and transformation activities.
- Agents and software versions.
- Generated graph artifacts.
- Derivation relationships.
- Validation results.
- Vocabulary and context dependencies.

RDF provides the graph substrate; W3C PROV provides a standard vocabulary for expressing the provenance graph.

## Design Notes

RDF gives EDT a durable interoperability layer across metadata, provenance, terminology, and linked-data systems. Its role is to expose selected document knowledge as a graph, not to replace the semantic document architecture.

The durable design boundary is:

```text
EDOM is the canonical semantic document model.
RDF is the canonical external graph model for linked assertions.
Profiles define the mapping between them.
```

## References

- W3C, *RDF 1.1 Concepts and Abstract Syntax*: https://www.w3.org/TR/rdf11-concepts/
- W3C, *RDF 1.2 Concepts and Abstract Data Model*, Candidate Recommendation Snapshot, 7 April 2026: https://www.w3.org/TR/rdf12-concepts/
- W3C, *RDF Schema 1.1*: https://www.w3.org/TR/rdf-schema/
- W3C, *RDF 1.2 Schema*, Candidate Recommendation: https://www.w3.org/TR/rdf12-schema/
