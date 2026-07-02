# ITS 2.0

## Purpose

The Internationalization Tag Set (ITS) Version 2.0 is a W3C Recommendation for attaching internationalization, translation, localization, and language-processing metadata to XML and HTML content.

For EDT, ITS 2.0 provides a standards-based bridge between semantic document content and multilingual processing. It identifies what should be translated, how text behaves, which terminology applies, what quality issues exist, and how localization metadata is inherited or overridden.

## Current Standard

ITS 2.0 is the current W3C Recommendation, published on 29 October 2013.

EDT profiles using ITS should record:

- ITS version.
- XML or HTML host format.
- Local and global rule sources.
- Selector language.
- External rule dependencies.
- Data categories used.
- Mapping rules to XLIFF or other localization formats.

## Adoption Decision

EDT classifies ITS 2.0 as **Adopt** for internationalization metadata and **Bridge** for XML, HTML, XLIFF, and language-processing workflows.

Rationale:

- ITS 2.0 provides standardized data categories for multilingual processing.
- It supports both local annotations and global rule-based selection.
- It integrates naturally with XML and HTML.
- It complements XLIFF, TBX, SRX, and EDOM without replacing them.

## Where EDT Uses ITS 2.0

- Marking content as translatable or non-translatable.
- Providing localization notes.
- Identifying terminology.
- Recording language and directionality.
- Describing inline elements.
- Attaching domain metadata.
- Applying locale filters.
- Recording provenance and external resources.
- Expressing localization quality issues and ratings.
- Recording machine-translation confidence.
- Declaring allowed characters and storage-size limits.
- Preparing content for XLIFF export.

## Where EDT Does Not Use ITS 2.0

ITS 2.0 is not EDT's canonical document model. It does not replace:

- EDOM hierarchy and semantic-node identity.
- Source-region provenance.
- The complete reference graph.
- Publication profiles.
- Translation-memory storage.
- Terminology-system governance.
- Preservation metadata.

The architectural boundary is:

```text
EDOM owns document semantics and structure.
ITS 2.0 annotates content for multilingual processing.
XLIFF carries active localization work.
TBX and SKOS manage terminology and concepts.
```

## Local and Global Rules

ITS data categories can be expressed locally on content or globally through rule elements and selectors.

EDT should preserve:

- Whether an annotation was local or rule-derived.
- The rule source and selector.
- Precedence and inheritance behavior.
- The effective value applied to each semantic node.
- Any conflict between local and global annotations.

Global rules are useful for applying policy across imported XML or HTML without rewriting every element. Local annotations are appropriate when the decision is specific to one content region.

## Mapping to EDOM

Representative mappings are:

| ITS 2.0 data category | EDOM meaning |
| --- | --- |
| Translate | Localization eligibility |
| Localization Note | Translator or reviewer guidance |
| Terminology | Link to a term or terminology concept |
| Directionality | Base text direction |
| Language Information | Language tag |
| Elements Within Text | Inline-code behavior |
| Domain | Subject or domain metadata |
| Text Analysis | Named entity or linguistic annotation |
| Locale Filter | Locale-dependent inclusion rule |
| Provenance | Agent and process provenance |
| External Resource | Linked external asset |
| Target Pointer | Location of target-language content |
| ID Value | Stable localization identifier |
| Preserve Space | Whitespace-preservation policy |
| Localization Quality Issue | Structured quality finding |
| Localization Quality Rating | Quality score or assessment |
| MT Confidence | Machine-translation confidence |
| Allowed Characters | Character-set constraint |
| Storage Size | Length or storage constraint |

EDT should store the effective semantic meaning in EDOM while preserving the original ITS expression for round-trip and audit.

## Translate

The Translate data category determines whether content is intended for translation.

EDT validation should detect:

- Missing translation policy where a profile requires one.
- Conflicting inherited and local values.
- Translatable child content inside a protected structure without a valid mapping.
- Non-translatable content incorrectly exported into an XLIFF target field.

## Localization Notes

Localization notes may describe meaning, audience, constraints, placeholders, tone, or usage.

EDT should distinguish notes intended for:

- Translators.
- Reviewers.
- Editors.
- Internal tooling.

Sensitive internal notes should not be exported to external localization systems unless the profile explicitly permits them.

## Terminology

ITS terminology annotations may identify a term occurrence and link it to terminology information.

EDT should connect term occurrences to stable TBX or SKOS concept identifiers when available. A terminology annotation should not become the authoritative terminology record merely because it appears in source markup.

## Language and Directionality

Language and base direction are semantic properties, not visual formatting.

EDT should preserve:

- Language tags.
- Script and region subtags where meaningful.
- Left-to-right or right-to-left direction.
- Language changes within content.
- Conflicts between inherited and explicit values.

## Elements Within Text

The Elements Within Text data category helps localization tools understand whether an element is part of a sentence, separates text flow, or behaves as an inline code.

This is critical when converting XML or HTML into XLIFF. EDT should map the result into reversible inline-code behavior rather than flattening markup into plain text.

## Domain and Locale Filters

Domain metadata supports terminology selection and translation-memory relevance. Locale filters control whether content applies to selected locales.

EDT profiles should define domain vocabularies and locale-filter evaluation rules. Locale-specific omission must remain distinguishable from source deletion.

## Quality and Machine Translation

ITS 2.0 includes data categories for localization quality issues, quality ratings, and machine-translation confidence.

EDT should preserve:

- The issue type.
- Severity.
- Responsible agent.
- Confidence or score scale.
- Source revision.
- Resolution state.

A machine-generated score must not be presented as human approval.

## Import Strategy

An ITS-aware importer should:

1. Identify the host format and ITS version.
2. Load local and external global rules.
3. Apply selectors under the declared query language.
4. Compute effective values using precedence and inheritance.
5. Map recognized data categories into EDOM.
6. Preserve original annotations, selectors, and rule sources.
7. Report invalid selectors, conflicts, and unsupported categories.
8. Record the importer, dependencies, and results as provenance.

External rule retrieval should be controlled and reproducible. Network-fetched rules should be cached, hashed, and versioned.

## Export Strategy

An ITS exporter should:

1. Select a declared host-format profile.
2. Decide whether each annotation is emitted locally or through global rules.
3. Preserve stable node identifiers.
4. Emit only data categories supported by the target profile.
5. Validate the host document and ITS markup.
6. Test the effective annotations after rule application.
7. Preserve the generated document, external rules, and validation report.

Export should report semantics that cannot be represented faithfully in the selected host format.

## Validation

EDT validation may include:

- Invalid ITS version declarations.
- Invalid XML or HTML usage.
- Broken external-rule references.
- Invalid XPath or CSS selectors.
- Conflicting local and global values.
- Unsupported data categories.
- Invalid language tags or direction values.
- Terminology links that do not resolve.
- Target pointers that do not resolve.
- Locale filters with invalid syntax.
- Quality metadata lacking required source or severity.
- Storage-size or allowed-character violations.
- XLIFF exports inconsistent with effective ITS annotations.

Markup validity alone does not prove that the intended effective annotations were produced.

## Relationship to XLIFF

ITS 2.0 annotates source content; XLIFF carries extracted localization units through translation and review.

An EDT XLIFF exporter should map effective ITS annotations into XLIFF notes, inline-code behavior, terminology references, constraints, quality metadata, and profile-specific extensions where the mapping is defined.

The mapping must be tested for reversibility and must report unsupported data categories.

## Relationship to NIF and RDF

ITS 2.0 defines mappings to the NLP Interchange Format for language-technology processing.

EDT may use RDF-based projections when a workflow requires linked linguistic annotations or named-entity data. Such projections should remain derived views with explicit provenance rather than replacing EDOM text identity.

## Profiles

An EDT ITS profile may specify:

- Host format.
- Allowed data categories.
- Local versus global annotation policy.
- Selector languages.
- External-rule policy.
- Inheritance and override rules.
- XLIFF mappings.
- TBX or SKOS terminology links.
- Locale-filter policy.
- Quality metadata policy.
- Validation fixtures.

## Design Rule

```text
Keep semantic structure in EDOM.
Attach multilingual processing intent with ITS 2.0.
Transfer localization work through XLIFF.
Preserve effective values and original rule provenance.
```

## References

- W3C, *Internationalization Tag Set (ITS) Version 2.0*: https://www.w3.org/TR/its20/
