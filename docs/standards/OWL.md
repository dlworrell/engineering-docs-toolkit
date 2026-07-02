# OWL

## Purpose

The Web Ontology Language (OWL) is a W3C standard for defining formal ontologies over RDF data. OWL adds machine-interpretable semantics for classes, properties, individuals, identity, equivalence, disjointness, restrictions, and logical relationships.

For EDT, OWL is the formal-ontology layer used only when a project requires reasoning or stronger semantic commitments than RDF, RDF Schema, SKOS, or profile validation can provide.

## Current Standard

The current W3C Recommendation is **OWL 2 Web Ontology Language, Second Edition**, published on 11 December 2012.

OWL 2 includes:

- A structural specification and functional-style syntax.
- Direct Semantics for description-logic-oriented reasoning.
- RDF-Based Semantics for OWL ontologies expressed as RDF graphs.
- Standard serializations and mappings to RDF graphs.
- The OWL 2 EL, QL, and RL profiles.

An EDT ontology profile should record:

- The OWL 2 profile or semantic regime.
- Ontology IRI and version IRI.
- Imported ontologies and exact versions.
- Serialization.
- Reasoner and version.
- Entailment and validation policy.
- Any local restrictions or extensions.

## Adoption Decision

EDT classifies OWL as **Evaluate** for general EDT use and **Adopt** only in profiles that require formal ontology reasoning.

Rationale:

- OWL provides semantics that RDF, RDFS, and SKOS do not provide.
- Formal reasoning can detect inconsistencies and infer relationships that would otherwise require custom code.
- OWL also introduces substantial modeling, performance, governance, and tooling complexity.
- Most document-engineering profiles need controlled vocabularies and validation, not unrestricted ontology reasoning.

EDT should therefore avoid making OWL a mandatory dependency of the core document pipeline.

## Where EDT Uses OWL

- Formal domain ontologies.
- Semantic integration across independently developed vocabularies.
- Machine reasoning over classes and properties.
- Consistency checking for ontology-backed profiles.
- Identity and equivalence assertions where their logical consequences are intended.
- Classification of entities into inferred classes.
- Interchange with ontology repositories, reasoners, and knowledge graphs.
- Engineering domains that already publish authoritative OWL ontologies.

## Where EDT Does Not Use OWL

OWL is not EDT's canonical document model. It does not replace EDOM's ordered hierarchy, text spans, source regions, page provenance, validation findings, publication profiles, or transformation pipeline.

OWL is also not the default mechanism for ordinary document validation. The open-world assumption and monotonic semantics differ from the closed-world checks commonly required for publication readiness.

The architectural boundary is:

```text
EDOM owns document structure and semantic processing.
RDF carries graph assertions.
OWL supplies optional formal ontology semantics and reasoning.
Profiles define where ontology reasoning is permitted and required.
```

## Core Modeling Concepts

Representative OWL constructs include:

| OWL construct | Purpose |
| --- | --- |
| Ontology | Identified collection of axioms and imports |
| Class | Category of individuals |
| Individual | Instance-level entity |
| Object property | Relationship between individuals |
| Data property | Relationship from an individual to a literal |
| Annotation property | Non-logical descriptive annotation |
| Subclass axiom | States that every member of one class is a member of another |
| Equivalent classes | States that class expressions have the same extension |
| Disjoint classes | States that classes cannot share members |
| Property domain and range | Logical implications about property subjects and objects |
| Restriction | Class expression based on property conditions |
| Property characteristic | Functional, inverse-functional, transitive, symmetric, asymmetric, reflexive, or irreflexive behavior |
| Same individual | Identity assertion |
| Different individuals | Distinctness assertion |
| Ontology import | Incorporation of another ontology's axioms |

These constructs have logical consequences. EDT documentation and profile authors must not treat them as informal labels.

## Mapping to EDT

Representative mappings are:

| EDT concept | OWL representation |
| --- | --- |
| Domain entity type | OWL class |
| Identified document entity | OWL individual |
| Typed EDOM relationship | Object property assertion |
| Literal metadata value | Data property assertion |
| Human-readable label or note | Annotation assertion |
| Profile-defined type hierarchy | Subclass axioms, when intended formally |
| Mutually exclusive semantic kinds | Disjoint-class axioms |
| External ontology alignment | Equivalent-class, equivalent-property, or mapping axioms where justified |
| Inferred classification | Reasoner-derived class assertion |
| Ontology-backed validation result | EDT validation finding with reasoner provenance |

EDOM kinds must not be converted mechanically into OWL classes unless the profile defines the formal meaning of that conversion.

## Open-World Assumption

OWL uses an open-world assumption: failure to prove a statement does not make the statement false.

For example, if a document contributor lacks an ORCID assertion, an OWL reasoner does not conclude that the contributor has no ORCID. It concludes only that the ontology does not establish one.

This differs from many EDT validation rules, which may require a field and report its absence.

EDT must therefore separate:

- Ontology consistency and entailment.
- Closed-world completeness checks.
- Publication-policy validation.
- Data-quality warnings.

OWL reasoning alone cannot replace EDT validation.

## No Unique-Name Assumption

OWL does not generally assume that two different IRIs identify different individuals.

Unless distinctness is asserted or logically implied, two identifiers may denote the same entity. Conversely, `owl:sameAs` states full logical identity and can propagate assertions broadly.

EDT should use `owl:sameAs` conservatively. Similar names, shared identifiers, or close correspondence are not sufficient grounds for asserting identity.

When weaker relationships are intended, profiles should use a more appropriate vocabulary term rather than `owl:sameAs`.

## Domain and Range Semantics

In OWL and RDF Schema, property domain and range declarations are inference rules, not merely input constraints.

If a property has domain `Person`, then using that property on a subject can entail that the subject is a `Person`.

EDT profiles must not use domain and range declarations as substitutes for validation rules unless those entailments are genuinely intended.

Closed-world checks should be implemented through EDT validation, SHACL, ShEx, or another declared constraint system.

## OWL 2 Profiles

OWL 2 defines three profiles optimized for common reasoning needs.

### OWL 2 EL

OWL 2 EL is designed for ontologies with large class and property hierarchies. It supports polynomial-time reasoning for core tasks and is well suited to large terminologies.

Potential EDT use:

- Large engineering or scientific terminologies.
- Classification-heavy domain models.
- Ontologies where scalable class reasoning matters more than expressive negation or universal restrictions.

### OWL 2 QL

OWL 2 QL is designed for query answering over large relational datasets. It supports rewriting ontology-aware queries into forms suitable for database execution.

Potential EDT use:

- Repository metadata integration.
- Ontology-mediated access to relational document inventories.
- Large institutional collections where query performance is central.

### OWL 2 RL

OWL 2 RL is designed for rule-based reasoning over RDF graphs. Many entailments can be implemented with forward-chaining rule systems.

Potential EDT use:

- Knowledge-graph enrichment.
- Rule-oriented metadata pipelines.
- Systems that need predictable reasoning over large RDF datasets.

Profiles must declare the selected OWL 2 profile and validate that ontology axioms remain within it.

## OWL 2 DL and OWL 2 Full

OWL 2 DL is the description-logic-oriented subset governed by the structural restrictions of the OWL 2 specification and interpreted using Direct Semantics.

OWL 2 Full refers to OWL interpreted through RDF-Based Semantics without the same structural restrictions. It is highly expressive, but complete reasoning is not generally decidable.

EDT should prefer a declared decidable profile or OWL 2 DL when automated reasoning is a required build step. OWL 2 Full should not be selected casually for production validation pipelines.

## Ontology Identity and Versioning

An ontology may have an ontology IRI and a version IRI.

EDT ontology profiles should preserve:

- Ontology IRI.
- Version IRI.
- Version information annotations.
- Import declarations.
- Retrieval source and time.
- Content fixity.
- License and governance metadata.

Builds should pin ontology dependencies to reproducible versions where possible. Importing whatever currently resolves from an ontology IRI creates non-reproducible validation and reasoning.

## Imports

OWL imports include the axioms of another ontology in the importing ontology's semantics.

EDT should treat imports as build dependencies. An ontology-enabled profile should define:

- How import IRIs are resolved.
- Whether network access is permitted.
- Local cache and lockfile behavior.
- Allowed ontology versions.
- Failure policy for unavailable imports.
- Cycle handling.
- Fixity verification.
- License and redistribution constraints.

Imported ontologies must be preserved or resolvable for archival reproducibility.

## Reasoning Strategy

An OWL-enabled EDT stage should:

1. Load the declared ontology and pinned imports.
2. Confirm the ontology fits the required OWL 2 profile.
3. Run the selected reasoner under a declared semantic regime.
4. Check ontology consistency.
5. Compute only the entailments required by the profile.
6. Keep asserted and inferred statements distinguishable.
7. Convert relevant inconsistencies or missing entailments into EDT findings.
8. Record the reasoner, version, configuration, ontology versions, runtime, and results.

Reasoner output should not silently rewrite authoritative EDOM fields. Inferences should be stored as derived assertions with provenance.

## Import Strategy

An OWL importer should preserve:

- Ontology and version IRIs.
- Imports.
- Axioms.
- Annotations.
- Prefix declarations.
- Serialization.
- Source graph and retrieval provenance.
- Profile membership.
- Unsupported or invalid axioms.

Imported ontology terms should remain identified by IRIs. Labels are presentation metadata and must not be substituted for identity.

## Export Strategy

An OWL exporter should:

1. Select a declared OWL 2 profile and serialization.
2. Generate stable IRIs.
3. Export only axioms justified by EDOM and the selected ontology profile.
4. Separate annotation metadata from logical axioms.
5. Preserve asserted versus inferred status where the package design supports it.
6. Validate profile conformance.
7. Run consistency checks when required.
8. Preserve the ontology, dependency lock information, and reasoner report as build artifacts.

EDT should report semantic loss when EDOM relationships cannot be represented faithfully in the selected profile.

## Serialization

OWL 2 supports several syntaxes and mappings, including:

- Functional-Style Syntax.
- RDF/XML.
- Turtle through the RDF mapping.
- OWL/XML.
- Manchester Syntax for human-oriented authoring and inspection.

An EDT profile must declare the interchange serialization. Tool-specific syntax support must not be mistaken for semantic-profile support.

## Validation

EDT OWL validation may include:

- Syntax and parsing errors.
- Missing ontology or version IRIs required by profile.
- Unresolved imports.
- Import-version drift.
- Axioms outside the selected OWL 2 profile.
- Ontology inconsistency.
- Unsatisfiable classes.
- Identity conflicts.
- Disjointness violations.
- Datatype errors.
- Unsupported reasoner features.
- Required entailments not established.
- Unexpected inferences produced by modeling errors.
- Use of logical axioms where annotations or validation rules were intended.

Ontology consistency does not prove publication completeness, data accuracy, or profile compliance.

## Relationship to RDF and RDF Schema

OWL ontologies may be represented as RDF graphs, but OWL adds semantics beyond plain RDF and RDFS.

RDF provides the graph model. RDFS provides lightweight class and property semantics. OWL provides richer ontology axioms and reasoning.

EDT profiles should use the least expressive standard that satisfies the requirement. More expressivity increases modeling risk and reasoning cost.

## Relationship to SKOS

SKOS is designed for practical concept schemes, thesauri, and taxonomies. OWL is designed for formal ontologies.

A SKOS concept is not automatically an OWL class. A project may combine SKOS and OWL, but any bridge between a concept scheme and a class ontology must be explicit.

Use SKOS when the requirement is primarily:

- Preferred and alternative labels.
- Broader, narrower, and related concepts.
- Classification notations.
- Vocabulary mappings.

Use OWL when the requirement includes formal logical axioms and machine reasoning.

## Relationship to SHACL and EDT Validation

OWL describes what follows logically from ontology axioms. SHACL and EDT validation describe whether a data graph or document satisfies declared constraints and policy.

Typical division:

```text
OWL: formal meaning and entailment.
SHACL or EDT validation: closed-world conformance and completeness.
EDOM: document semantics and source provenance.
```

A profile may use all three, but their findings must remain distinguishable.

## Profiles

An EDT OWL profile may specify:

- Ontology IRI and version IRI.
- Required import closure.
- OWL 2 profile.
- Semantic regime.
- Allowed axiom types.
- Required classes and properties.
- IRI policy.
- Reasoner and version.
- Materialization policy.
- Required entailments.
- Consistency and satisfiability checks.
- Constraint-validation language.
- Serialization.
- Dependency locking and offline behavior.
- Governance and ontology-release process.

## Provenance

Ontology reasoning is a transformation and must be reproducible.

EDT should record:

- Source ontology files and hashes.
- Import closure and versions.
- Reasoner and software version.
- Configuration and selected profile.
- Asserted input graph.
- Inferred output graph or selected entailments.
- Consistency and satisfiability results.
- Runtime warnings and errors.
- Human review or override decisions.

W3C PROV may be used to represent the reasoning activity and its derivations.

## Design Notes

OWL is powerful, but its role in EDT must remain disciplined. It is appropriate when the project genuinely needs formal ontology semantics and automated reasoning. It is excessive when a controlled vocabulary or validation schema would solve the problem more clearly.

The durable design rule is:

```text
Use SKOS for controlled concepts.
Use RDF for graph interchange.
Use OWL for formal ontology semantics.
Use EDT validation or a constraint language for publication conformance.
```

## References

- W3C, *OWL 2 Web Ontology Language Document Overview (Second Edition)*: https://www.w3.org/TR/owl2-overview/
- W3C, *OWL 2 Web Ontology Language Structural Specification and Functional-Style Syntax (Second Edition)*: https://www.w3.org/TR/owl2-syntax/
- W3C, *OWL 2 Web Ontology Language Profiles (Second Edition)*: https://www.w3.org/TR/owl2-profiles/
- W3C, *OWL 2 Web Ontology Language Direct Semantics (Second Edition)*: https://www.w3.org/TR/owl2-direct-semantics/
- W3C, *OWL 2 Web Ontology Language RDF-Based Semantics (Second Edition)*: https://www.w3.org/TR/owl2-rdf-based-semantics/
