# SHACL

## Purpose

SHACL (Shapes Constraint Language) is a W3C standard for describing and validating RDF graphs. It defines shapes that select focus nodes, constrain their properties and values, and produce machine-readable validation reports.

For EDT, SHACL is the standards-based validation layer for RDF exports and linked-data profiles. It complements EDT's native semantic validation without replacing it.

## Current Standard

The stable standard is the W3C Recommendation published on 20 July 2017.

SHACL 1.2 Core is under active development on the W3C Recommendation track. The 30 June 2026 publication is a Working Draft, so EDT must treat it as experimental rather than production-stable.

EDT therefore adopts the 2017 Recommendation for production interchange and evaluates SHACL 1.2 for future adoption.

## Adoption Decision

EDT classifies SHACL as **Adopt** for RDF graph validation and **Bridge** for external linked-data conformance.

Rationale:

- It is the stable W3C standard for graph constraints.
- It produces structured validation reports that map well to EDT findings.
- It supports cardinality, datatypes, classes, node kinds, ranges, patterns, logical constraints, property relationships, and closed shapes.
- It provides closed-world conformance checks without forcing OWL reasoning to serve as a validation language.

## Core Model

SHACL validation operates on two RDF graphs:

| Graph | Purpose |
| --- | --- |
| Data graph | The RDF graph being validated |
| Shapes graph | The RDF graph containing targets, shapes, and constraints |

Representative concepts include:

| SHACL concept | Purpose |
| --- | --- |
| Node shape | Constrains a focus node as a whole |
| Property shape | Constrains values reached through a property path |
| Target | Selects nodes to validate |
| Focus node | Node currently being validated |
| Value node | Value reached from a focus node through a path |
| Constraint component | Reusable validation rule type |
| Severity | Violation, Warning, Info, or profile-defined severity |
| Validation result | One reported constraint failure |
| Validation report | RDF graph summarizing conformance and results |

## Where EDT Uses SHACL

- Validation of RDF exports.
- Validation of SKOS concept schemes.
- Validation of Schema.org, Dublin Core, W3C PROV, and other RDF metadata profiles.
- Validation of linked identifiers and graph relationships.
- Repository or publisher graph-conformance checks.
- Machine-readable exchange of graph-validation findings.

## Where EDT Does Not Use SHACL

SHACL is not EDT's canonical document validator. EDT native validation remains responsible for EDOM hierarchy, source-region integrity, reference-graph consistency, provenance, publication invariants, and rules that depend on document order or non-RDF build state.

The boundary is:

```text
EDT validation owns semantic document conformance.
SHACL owns RDF graph conformance.
Adapters map SHACL results into EDT quality reports.
```

## Mapping to EDT Validation

| SHACL | EDT validation |
| --- | --- |
| Shape | Profile-defined validation rule group |
| Target | Rule applicability selector |
| Focus node | Subject of a finding |
| Result path | Affected property or relationship |
| Value | Offending value |
| Source shape | Rule identifier or origin |
| Result message | Human-readable finding message |
| Severity | EDT finding severity |
| Validation report | Graph-validation evidence artifact |
| `sh:conforms` | Overall graph-conformance status |

EDT should preserve the complete SHACL result graph as well as the normalized EDT findings derived from it.

## Constraint Strategy

Profiles should prefer SHACL Core where it is expressive enough. Core is the portability baseline and covers:

- Classes, datatypes, and node kinds.
- Minimum and maximum counts.
- Numeric ranges.
- String lengths and patterns.
- Language constraints.
- Property equality, disjointness, and ordering.
- Logical combinations.
- Nested shapes.
- Qualified value counts.
- Closed shapes.
- Required and enumerated values.

SHACL-SPARQL may be used for complex graph-pattern checks, but only when Core cannot express the rule clearly. Profiles using SHACL-SPARQL must record the query text, processor, limits, and security policy.

## Targets and Paths

Targets determine which graph nodes a shape validates. A valid constraint provides no protection if the intended nodes are not selected.

Property shapes may use direct, sequence, alternative, inverse, and repeated paths. Complex paths should be documented because they can obscure intent and increase processing cost.

## Closed Shapes

Closed shapes restrict which properties may appear on a focus node. They are useful for strict interchange profiles but can conflict with extensible linked-data practices.

An EDT profile must declare whether unknown properties are rejected, warned about, preserved as extensions, or allowed within named namespaces.

## Severity

The default EDT mapping is:

| SHACL severity | EDT severity |
| --- | --- |
| `sh:Violation` | Error |
| `sh:Warning` | Warning |
| `sh:Info` | Information |

Profiles may override this mapping, but must preserve the original SHACL severity IRI.

## Validation Reports

A SHACL validation report can identify:

- Overall conformance.
- Focus node.
- Result path.
- Value node.
- Source shape.
- Source constraint component.
- Message.
- Severity.
- Nested details.

EDT should retain both the RDF report and its normalized findings. Raw report bytes should not be used as the only regression comparison because ordering, blank-node identifiers, and generated messages may vary across processors.

## Entailment

Profiles must declare whether validation sees only explicit triples or also applies RDFS, OWL, pre-materialized inference, or another rule set.

A result may change when entailment changes, so the entailment regime is part of validation provenance.

## Relationship to OWL

OWL and SHACL answer different questions:

```text
OWL: ontology meaning, consistency, and entailment.
SHACL: closed-world RDF graph conformance.
EDT validation: semantic document and workflow conformance.
```

An OWL-consistent graph may fail SHACL, and a SHACL-conforming graph may still be incomplete under a publication profile.

## Relationship to SKOS and Schema.org

SKOS defines concept schemes; SHACL can validate project-specific rules over them, such as label cardinality, scheme membership, definitions, notations, and mapping provenance.

Schema.org defines a broad vocabulary; SHACL can define a narrower EDT publication profile requiring identifiers, authors, dates, part-whole relationships, or accessibility metadata.

These constraints are EDT profile rules, not universal requirements of SKOS or Schema.org.

## Import Strategy

A SHACL importer should preserve:

- Shapes-graph serialization.
- Base IRI and prefixes.
- Shape identifiers and targets.
- Node and property shapes.
- Paths and constraints.
- Messages and severities.
- SPARQL constraints and extensions.
- Deactivation state.
- Source and retrieval provenance.

Untrusted shapes must not execute automatically. Profiles must define review and sandboxing policy.

## Export Strategy

An EDT SHACL exporter should:

1. Select a declared SHACL version and feature set.
2. Generate stable shape identifiers.
3. Map profile rules into SHACL Core where possible.
4. Use SHACL-SPARQL only when justified.
5. Attach clear messages and severities.
6. Validate the shapes graph itself.
7. Test conforming and nonconforming fixtures.
8. Preserve the shapes graph and test evidence.

Not every EDT validation rule can be exported to SHACL. Unsupported rules must be reported rather than silently omitted.

## Processor and Security Policy

An EDT profile should declare:

- SHACL Core or SHACL-SPARQL support.
- Entailment regime.
- Recursive-shape behavior.
- Processor and version.
- Time and memory limits.
- Required validation-report fields.

SPARQL and implementation-specific extensions may consume substantial resources. EDT should apply timeouts, resource limits, network restrictions, and review requirements for untrusted shapes.

## SHACL Advanced Features

The 2017 SHACL Advanced Features document is a W3C Working Group Note, not a Recommendation. It covers custom targets, annotation properties, functions, node expressions, expression constraints, and rules.

EDT classifies these features as **Evaluate** unless a profile explicitly requires them and pins a tested processor.

## SHACL 1.2 Readiness

SHACL 1.2 is a Working Draft. Potentially relevant areas include new target mechanisms, list constraints, reification-aware constraints, additional shape metadata, and revised conformance controls.

Experimental EDT profiles may evaluate these features only when they:

- Identify the dated draft.
- Pin the processor version.
- Use isolated fixtures.
- Record processor-specific behavior.
- Provide compatibility analysis against the stable Recommendation.

## Validation Workflow

A recommended EDT stage is:

1. Load the declared profile and locked dependencies.
2. Validate the shapes graph.
3. Generate or load the RDF data graph from validated EDOM.
4. Apply the declared entailment regime.
5. Run the selected SHACL processor.
6. Preserve the complete RDF validation report.
7. Normalize results into EDT findings.
8. Apply severity and build-failure policy.
9. Record versions, hashes, configuration, and outcomes in provenance.

## Profiles

An EDT SHACL profile may specify:

- SHACL version.
- Core-only or SPARQL-enabled conformance.
- Shape and vocabulary dependencies.
- Target policy.
- Severity mapping.
- Closed-shape policy.
- Entailment regime.
- Processor and version.
- Time and resource limits.
- Report requirements.
- Test fixtures.
- Draft-feature policy.

## Design Notes

SHACL gives EDT a portable graph-validation layer without replacing EDOM validation.

```text
Validate documents in EDOM.
Validate RDF projections with SHACL.
Preserve both result models and their provenance.
```

## References

- W3C, *Shapes Constraint Language (SHACL)*, Recommendation, 20 July 2017: https://www.w3.org/TR/shacl/
- W3C, *SHACL Advanced Features*, Working Group Note, 8 June 2017: https://www.w3.org/TR/shacl-af/
- W3C, *SHACL 1.2 Core*, Working Draft, 30 June 2026: https://www.w3.org/TR/shacl12-core/
