# PREMIS

## Purpose

PREMIS (Preservation Metadata: Implementation Strategies) defines implementable metadata for preserving digital objects over time. It focuses on the information a repository needs to maintain viability, renderability, understandability, authenticity, identity, and long-term usability.

For EDT, PREMIS is the principal preservation-metadata bridge for archival packages, reproducible transformations, fixity records, preservation events, agents, rights, and relationships among preserved objects.

## Current Standard

The current PREMIS Data Dictionary is version 3.0. The standard consists of the Data Dictionary, an XML schema, conformance guidance, controlled vocabularies, examples, and supporting documentation.

An EDT preservation profile should record:

- The PREMIS version and schema used.
- The serialization and packaging convention.
- The repository or preservation system profile.
- Controlled-vocabulary versions.
- Conformance decisions and local extensions.

## Core PREMIS Entities

PREMIS 3.0 organizes preservation metadata around four principal entities:

| PREMIS entity | Purpose |
| --- | --- |
| Object | A digital object being preserved, including intellectual entities, representations, files, and bitstreams |
| Event | An action affecting or assessing an object, such as ingestion, validation, migration, normalization, or fixity checking |
| Agent | A person, organization, or software system associated with an event, object, or rights statement |
| Rights | Permissions, restrictions, statutes, licenses, or policies governing preservation actions |

Relationships connect these entities and record how preservation history, responsibility, derivation, and permissions fit together.

## Where EDT Uses PREMIS

- Preservation packages for source documents and generated publications.
- Fixity and integrity metadata.
- Recording imports, normalization, validation, transformation, and publication events.
- Recording software, people, organizations, and automated services as agents.
- Preserving relationships between source, normalized, derivative, and published objects.
- Documenting preservation rights and restrictions.
- Export to digital repositories and archival systems.
- Long-term auditability of document-engineering workflows.

## Where EDT Does Not Use PREMIS

PREMIS is not EDT's canonical semantic document model. It does not represent the complete hierarchy and meaning of chapters, paragraphs, equations, figures, tables, references, profiles, or source regions.

EDOM remains authoritative for document semantics and internal provenance. PREMIS receives a preservation-oriented projection of selected EDOM entities, artifacts, agents, events, rights statements, identifiers, and relationships.

PREMIS also does not replace W3C PROV. The two standards overlap in provenance concerns but serve different primary use cases:

- PREMIS is optimized for operational digital preservation.
- W3C PROV is a general provenance model for entities, activities, agents, and derivations.

EDT may emit both when a repository or workflow benefits from each representation.

## Mapping to EDT and EDOM

Representative mappings are:

| EDT / EDOM concept | PREMIS mapping |
| --- | --- |
| Source file | Object: file |
| Embedded stream or component | Object: bitstream |
| Complete publication package | Object: representation |
| Conceptual work or edition | Object: intellectual entity, where used by the target profile |
| Import operation | Event |
| Normalization operation | Event |
| Semantic validation | Event |
| Fixity check | Event |
| Publication build | Event |
| Format migration | Event |
| Human editor | Agent: person |
| EDT installation or publisher | Agent: software |
| Organization operating the workflow | Agent: organization |
| Source-to-derivative relationship | Object relationship |
| Hash and algorithm | Object characteristics / fixity |
| License or preservation permission | Rights entity |
| Source URI, DOI, UUID, or repository ID | Object or entity identifier |

The mapping should preserve distinctions among intellectual entities, representations, files, and bitstreams where the preservation profile uses them.

## Preservation Event Strategy

Every preservation-significant EDT operation should be representable as an event. A preservation event record should include:

- A stable event identifier.
- Event type.
- Date and time.
- Event detail or parameters.
- Outcome and outcome detail.
- Linked objects.
- Responsible agents.
- Software version and execution environment where relevant.
- Evidence artifacts such as logs, reports, manifests, or validation output.

Examples include:

- Ingestion.
- Virus or malware scanning.
- Format identification.
- Characterization.
- Fixity generation and checking.
- Semantic import.
- Normalization.
- Validation.
- Migration.
- Publication.
- Packaging.
- Replication.
- Deaccession or deletion under policy.

Event names should follow a declared controlled vocabulary where practical.

## Fixity and Integrity

EDT preservation packages should record cryptographic digests for preserved files and generated artifacts. The record should include:

- The digest value.
- The algorithm.
- The object to which it applies.
- The date and context of calculation.
- The responsible agent or software.
- Subsequent verification events and outcomes.

A manifest alone is insufficient unless its creation, scope, algorithm, and verification history are also preserved.

EDT should distinguish:

- Source-file fixity.
- Imported or normalized EDOM serialization fixity.
- Generated publication fixity.
- Package-manifest fixity.
- Remote-resource evidence captured during a snapshot or site-proof workflow.

## Object Relationships

Preservation packages should represent derivation and composition explicitly. Typical relationships include:

- A normalized object derived from a source file.
- A publication derived from a validated EDOM document.
- A representation composed of multiple files.
- A file containing one or more bitstreams.
- A migrated object replacing or supplementing an earlier format.
- A static web snapshot derived from a retrieved web resource.
- A corrected edition related to an earlier publication.

These relationships should align with EDT's reference graph and provenance model rather than being inferred after publication.

## Rights

PREMIS rights metadata should be used for preservation actions, not as a replacement for the complete legal or descriptive rights record.

An EDT preservation profile may record:

- The basis for permission, such as license, statute, policy, or donor agreement.
- The actions permitted.
- Restrictions or conditions.
- Applicable dates.
- Linked documents or evidence.
- The objects covered by the permission.

Sensitive legal documents or credentials should not be embedded directly when a protected reference is more appropriate.

## Import Strategy

When importing PREMIS metadata, EDT should preserve:

- Entity identifiers.
- Object hierarchy and relationships.
- Events and outcomes.
- Agents and their roles.
- Rights statements.
- Controlled-vocabulary values.
- Local extensions.
- The PREMIS version, schema, and source package.
- Source locations and retrieval provenance.

Imported PREMIS assertions should not silently override stronger local evidence. Conflicts should be retained and reported.

## Export Strategy

A PREMIS exporter should:

1. Select a declared preservation profile and serialization.
2. Identify the objects included in the package.
3. Generate stable identifiers.
4. Record fixity and technical characteristics.
5. Convert EDT workflow history into preservation events.
6. Link events to objects and agents.
7. Export applicable rights metadata.
8. Validate against the selected PREMIS schema and profile.
9. Preserve the generated PREMIS record, validation output, and package manifest.

Exporters must report semantic loss, omitted history, unsupported local extensions, and profile constraints.

## Packaging

PREMIS is often used with packaging or structural standards rather than as a complete package format by itself. EDT profiles may combine PREMIS with standards or conventions such as:

- METS.
- BagIt.
- OCFL.
- Repository-specific archival information packages.
- W3C PROV.
- Dublin Core or another descriptive metadata vocabulary.

The package profile must define which standard owns each class of information and how identifiers connect the records.

## Validation

EDT validation may include:

- Missing object identifiers.
- Missing or unsupported fixity algorithms.
- Digest mismatches.
- Events without linked objects or agents.
- Objects without format information required by a profile.
- Broken derivation or composition relationships.
- Invalid dates or event sequences.
- Rights statements that do not identify applicable actions or objects.
- Unsupported controlled-vocabulary terms.
- Schema or profile conformance failures.
- Generated artifacts not represented in the preservation record.
- Preservation assertions lacking evidence or provenance.

Schema validity alone does not prove that a preservation record is complete or operationally useful.

## Profiles

An EDT PREMIS profile may specify:

- Required object levels.
- Identifier policy.
- Required fixity algorithms.
- Required event types.
- Controlled vocabularies.
- Agent-identification rules.
- Rights requirements.
- Package structure.
- Required technical metadata.
- Use of METS, BagIt, OCFL, or repository-specific packaging.
- Relationship to W3C PROV.
- Conformance and validation procedures.

## Provenance Boundary

EDT's internal provenance can be more granular than a preservation repository needs. For example, EDT may track source regions, individual semantic transformations, validation findings, and reference-graph changes.

The PREMIS export should preserve the subset necessary to explain and verify the preservation history of the archived objects while retaining links to richer EDT evidence artifacts when available.

The architectural boundary is:

```text
EDOM owns document semantics and detailed transformation provenance.
PREMIS records the preservation state, history, agents, rights, and integrity of archived objects.
```

## Adoption Decision

EDT classifies PREMIS as **Adopt** for preservation metadata and **Bridge** for repository interchange.

Rationale:

- It is the established international standard for implementable digital-preservation metadata.
- It models the objects, events, agents, rights, fixity, and relationships EDT must preserve.
- It complements rather than replaces EDOM and W3C PROV.
- It supports long-term auditability without requiring EDT to invent a proprietary archival vocabulary.

## References

- Library of Congress, *PREMIS: Preservation Metadata Maintenance Activity*: https://www.loc.gov/standards/premis/
- PREMIS Editorial Committee, *PREMIS Data Dictionary for Preservation Metadata, Version 3.0*: https://www.loc.gov/standards/premis/v3/premis-3-0-final.pdf
- Library of Congress, *PREMIS Version 3.0 schemas and documentation*: https://www.loc.gov/standards/premis/v3/
