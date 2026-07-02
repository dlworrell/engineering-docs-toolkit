# XLIFF

## Purpose

XLIFF (XML Localization Interchange File Format) is an OASIS XML vocabulary for carrying localizable content and related localization metadata between tools and stages of a translation workflow.

For EDT, XLIFF is the principal interchange format for extracting translatable content from semantic documents, sending that content through localization systems, and merging reviewed translations back into EDOM without losing identity, inline structure, provenance, or publication intent.

## Current Specifications

The XLIFF 2.x family separates the specification into a Core and an Extended part.

As of July 2026:

- **XLIFF 2.1** is the current OASIS Standard.
- **XLIFF 2.2** is the latest OASIS Committee Specification, published on 13 March 2025.
- **XLIFF 1.2** remains common in legacy localization tools and interchange workflows.

EDT adopts the following policy:

- **Adopt XLIFF 2.1** as the default production interchange target until 2.2 support is sufficiently common across the selected toolchain.
- **Evaluate and support XLIFF 2.2 through an explicit profile** where its features are required and every participating tool declares compatible support.
- **Bridge XLIFF 1.2** for legacy import and export, with explicit loss and compatibility reporting.

Every localization job must record the XLIFF version, namespace, modules, profile, source language, target language, segmentation policy, and toolchain versions used.

## Adoption Decision

EDT classifies XLIFF as **Adopt** for localization interchange and **Bridge** for translation-management and computer-assisted translation ecosystems.

Rationale:

- It separates localizable content from source-format engineering.
- It preserves source and target text, segmentation, inline codes, states, notes, and identifiers.
- It supports modular metadata for matches, glossaries, formatting, validation, resource data, size restrictions, ITS data, and plural/gender/select behavior.
- It allows EDT to integrate with established localization tools instead of inventing a proprietary translation package.
- It complements EDOM without replacing the canonical semantic document model.

## Where EDT Uses XLIFF

- Export of translatable document content.
- Import of translated or reviewed target content.
- Exchange with translation-management systems.
- Exchange with computer-assisted translation tools.
- Preservation of segment identity across localization cycles.
- Inline-code protection.
- Translator notes and contextual metadata.
- Translation state and review status.
- Candidate translation and glossary information.
- Validation of localization-package completeness.
- Multilingual publication builds.

## Where EDT Does Not Use XLIFF

XLIFF is not EDT's canonical document representation. It does not replace:

- EDOM hierarchy and semantic object types.
- Source-region and page provenance.
- The complete reference graph.
- Publication profiles.
- Full asset management.
- Preservation metadata.
- General provenance history.
- Terminology systems whose authoritative form is TBX, SKOS, or another vocabulary.
- Translation-memory repositories whose authoritative exchange format is TMX or a system-native database.

The architectural boundary is:

```text
EDOM owns document meaning, structure, identity, and provenance.
XLIFF carries a controlled localization projection of that content.
```

## Core XLIFF Concepts

Representative XLIFF 2.x concepts include:

| XLIFF concept | Purpose |
| --- | --- |
| `xliff` | Root localization package |
| `file` | Content associated with one original resource or logical source unit |
| `group` | Hierarchical grouping of localization units |
| `unit` | Stable localization unit containing segments or ignorable content |
| `segment` | Translatable source and target pair |
| `ignorable` | Non-translatable content retained for context or reconstruction |
| `source` | Source-language content |
| `target` | Target-language content |
| Inline codes | Protected structure embedded within text |
| Notes | Human-readable context or instruction |
| State metadata | Translation and review progression |
| Modules | Standardized extensions for specialized localization information |

XLIFF unit and segment boundaries are localization constructs. They are not automatically equivalent to EDOM node boundaries.

## Mapping to EDOM

Representative mappings are:

| EDOM concept | XLIFF mapping |
| --- | --- |
| Document or publication | One localization package or package set |
| Source resource | `file` |
| Section or logical grouping | `group`, where useful |
| Translatable semantic node | `unit` |
| Translation segment | `segment` |
| Source text | `source` |
| Target-language text | `target` |
| Inline semantic object | Protected inline code or annotation |
| Stable EDOM identifier | XLIFF unit identifier plus EDT metadata |
| Source region | EDT extension metadata or linked provenance artifact |
| Translator instruction | Note |
| Translation status | State and review metadata |
| Glossary concept | Glossary module reference or linked terminology resource |
| Validation finding | Validation module data or linked EDT report |
| Translation candidate | Translation Candidates module |
| Character or layout limit | Size and Length Restriction module |
| Plural/gender/select variant | Plural, Gender, and Select module in a compatible 2.2 profile |

The export mapping must remain reversible enough to identify the originating EDOM node and merge the target text safely.

## Localization Unit Policy

EDT should not create XLIFF units by blindly splitting visible text.

A unit boundary should reflect a stable localization responsibility, such as:

- A paragraph.
- A heading.
- A caption.
- A list item.
- A table cell.
- A figure label.
- A note.
- A user-interface string.
- A profile-defined semantic field.

A semantic object may contain multiple segments. Segmentation can change during localization without changing the identity of the containing unit.

EDT must preserve the distinction between:

- EDOM node identity.
- XLIFF unit identity.
- Segment identity.
- Source text revision.
- Target-language revision.

## Stable Identity

Every exported unit must have a stable identifier that can be traced back to the originating EDOM object.

Identifiers should:

- Remain stable across publication-format changes.
- Remain stable across harmless source reflow or pagination changes.
- Change or receive a new revision relationship when the semantic source changes materially.
- Avoid dependence on ordinal position alone.
- Be unique within the localization package and resolvable through EDT metadata.

A localization merge must fail safely when a returned unit cannot be matched unambiguously to the expected EDOM source revision.

## Source Revision and Staleness

Translations can become stale when the source text changes.

EDT should record, for each exported unit:

- Source-text digest.
- Source-language value.
- EDOM node identifier.
- EDOM document revision.
- Export time.
- Profile and segmentation policy.
- Relevant inline-code structure.

On import, EDT should compare the returned package with the current source. Changed source units must be classified according to policy, for example:

- Unchanged and safe to merge.
- Changed only in non-translatable metadata.
- Changed in whitespace or segmentation.
- Changed semantically and requiring review.
- Deleted or superseded.
- Newly introduced.

EDT must not silently apply a target translation to materially different source content.

## Inline Content

Inline codes protect non-text structure that appears within a translatable span, such as:

- Emphasis.
- Links.
- Cross-references.
- Variables.
- Placeholders.
- Mathematical fragments.
- Index markers.
- Footnote anchors.
- Semantic annotations.
- Application-specific tokens.

An EDT exporter should use the appropriate XLIFF inline-code model and retain enough metadata to reconstruct the EDOM structure.

Validation should detect:

- Missing codes.
- Duplicate codes.
- Reordered codes where order is constrained.
- Invalid nesting or pairing.
- Modified protected data.
- Target text that references deleted source structures.

Rendered markup should not be exposed as freely editable text when a protected inline representation is available.

## Segmentation

Segmentation divides a unit into translation segments. It may be performed by EDT, a translation-management system, or a localization tool according to a declared policy.

EDT should record:

- Whether segmentation was source-defined or tool-generated.
- Segmentation rules and versions.
- Original unit boundaries.
- Segment identifiers.
- Merge and split history where available.

Returned segmentation must not be mistaken for semantic document structure. A sentence split is not necessarily a new EDOM paragraph, and merged translation segments do not necessarily merge source semantic nodes.

## Language and Direction

Each localization job must declare source and target languages using valid language tags.

EDT should preserve:

- Language tags.
- Script and region subtags where meaningful.
- Base direction.
- Inline bidirectional controls or annotations.
- Language changes within a unit.
- Target-specific typography rules supplied by the publication profile.

Language identification and text direction are semantic properties, not merely visual formatting.

## Notes and Context

Translation quality depends on context. EDT may export notes containing:

- Semantic role.
- Document title and section path.
- Figure or table context.
- Audience.
- Domain.
- Definition or glossary reference.
- Character limits.
- Placeholder explanation.
- Cross-reference target description.
- Accessibility purpose.
- Whether text is visible, spoken, indexed, or machine-consumed.

Sensitive or irrelevant source information should not be included merely because it is available in EDOM.

## XLIFF 2.x Modules

XLIFF 2.2 Part 2 defines the Extended specification and standard modules. EDT profiles may use modules only when participating tools support them.

Relevant modules include:

| Module | EDT use |
| --- | --- |
| Translation Candidates | Suggested translations and match metadata |
| Glossary | Package-local terminology guidance |
| Format Style | Formatting-related localization metadata |
| Metadata | Structured extension metadata |
| Resource Data | References to original resource information |
| Size and Length Restriction | Character, storage, or display constraints |
| Validation | Target-content validation requirements |
| ITS | Internationalization Tag Set mappings and data categories |
| Plural, Gender, and Select | Structured language-selection variants in XLIFF 2.2 profiles |

Module use must be declared. Unsupported modules must not be silently discarded during import or round-trip.

## Import Strategy

An XLIFF importer should preserve:

- XLIFF version and namespace.
- Core and module data.
- Source and target languages.
- File, group, unit, and segment identifiers.
- Source and target content.
- Inline codes and annotations.
- Notes.
- Translation states.
- Match, glossary, validation, and restriction data.
- Original-resource references.
- Extension namespaces and unknown extension content.
- Source package fixity and import provenance.

Before merging target content into EDOM, the importer should:

1. Validate the XLIFF document and declared modules.
2. Verify package identity and expected source revision.
3. Match units to EDOM objects.
4. Compare source text and inline structures.
5. Detect stale, missing, duplicate, or unexpected units.
6. Validate target content and protected codes.
7. Apply only changes permitted by the merge policy.
8. Record the merge as a provenance activity.
9. Produce a localization merge report.

Unknown extensions should be retained as typed extension data where practical and reported when they affect merge safety.

## Export Strategy

An XLIFF exporter should:

1. Select a declared XLIFF version and profile.
2. Select the source and target language pair.
3. Determine eligible translatable EDOM nodes.
4. Assign stable file, group, unit, and segment identifiers.
5. Protect inline semantic structures.
6. Export contextual notes and constraints.
7. Record source digests and EDOM revision metadata.
8. Validate the generated package.
9. Preserve the package, configuration, and validation report as build artifacts.

The exporter should report:

- Content omitted as non-translatable.
- EDOM structures approximated in XLIFF.
- Unsupported modules.
- Inline constructs that could not be protected safely.
- Data that requires a proprietary extension.

## XLIFF 1.2 Compatibility

XLIFF 1.2 remains widespread, but its data model differs materially from XLIFF 2.x.

An EDT XLIFF 1.2 profile should:

- Declare 1.2 explicitly.
- Map EDOM units to `trans-unit` structures deliberately.
- Preserve inline-code semantics using compatible 1.2 constructs.
- Avoid pretending that 2.x modules exist in 1.2.
- Report data lost or flattened during conversion.
- Preserve legacy identifiers and tool extensions.
- Validate against the XLIFF 1.2 schema and the receiving tool's business rules.

Conversion between 1.2 and 2.x should be treated as a provenance-recorded transformation, not as a namespace substitution.

## Translation Memory and Terminology

XLIFF can carry candidates and glossary information, but it is not a complete replacement for dedicated translation-memory or terminology exchange.

Recommended boundary:

```text
XLIFF carries the localization job.
TMX exchanges translation-memory units.
TBX or SKOS exchanges managed terminology.
EDOM owns the source and localized document semantics.
```

Profiles may package links or snapshots from translation-memory and terminology systems, but authoritative ownership must be explicit.

## Validation

EDT XLIFF validation may include:

- XML and schema errors.
- Namespace and version mismatches.
- Unsupported modules.
- Missing source or target language declarations.
- Duplicate file, unit, or segment identifiers.
- Units that cannot be mapped to EDOM.
- Stale source digests.
- Missing or unexpected units.
- Modified protected inline codes.
- Invalid code pairing or nesting.
- Missing required targets.
- Invalid language tags.
- Target text violating size or validation constraints.
- Translation states inconsistent with content.
- Unknown extensions affecting merge safety.
- Target content identical to source where a profile requires review.
- References, placeholders, or variables damaged in translation.

Schema validity alone is insufficient. A package may be valid XLIFF while still being stale, incomplete, mismatched to the document revision, or unsafe to merge.

## Profiles

An EDT XLIFF profile may specify:

- XLIFF version.
- Core-only or Core-plus-module conformance.
- Source and target language policy.
- Unit extraction rules.
- Segmentation policy.
- Identifier construction.
- Inline-code mapping.
- Notes and context policy.
- Translation-state workflow.
- Required modules.
- Extension namespaces.
- Character and layout restrictions.
- Validation rules.
- Merge conflict policy.
- Legacy XLIFF 1.2 compatibility.
- Translation-management-system constraints.

Profiles must be versioned and preserved with the localization package.

## Provenance

Localization is a transformation process and must be auditable.

EDT should record:

- Source EDOM revision.
- Exported XLIFF artifact and digest.
- XLIFF version and profile.
- Source and target languages.
- Exporter and version.
- Translation system and tool versions where available.
- Human or organizational agents responsible for translation and review.
- Returned XLIFF artifact and digest.
- Merge decisions and conflicts.
- Resulting localized EDOM revision.
- Validation and quality reports.

W3C PROV may describe the localization activities and derivations, while PREMIS may record preservation-significant package events.

## Design Notes

XLIFF allows EDT to keep document semantics separate from localization-tool interchange. The critical design requirement is safe round-trip identity: translated text must return to the correct semantic object and source revision without damaging protected structure.

The durable boundary is:

```text
EDOM is the source of truth for multilingual document semantics.
XLIFF is the source of truth for one declared localization interchange transaction.
```

## References

- OASIS, *XLIFF Version 2.2. Part 1: Core*, Committee Specification, 13 March 2025: https://docs.oasis-open.org/xliff/xliff-core/v2.2/xliff-core-v2.2-part1.html
- OASIS, *XLIFF Version 2.2. Part 2: Extended*, Committee Specification, 13 March 2025: https://docs.oasis-open.org/xliff/xliff-core/v2.2/xliff-extended-v2.2-part2.html
- OASIS, *XLIFF Version 2.1*, OASIS Standard, 13 February 2018: https://docs.oasis-open.org/xliff/xliff-core/v2.1/xliff-core-v2.1.html
- OASIS, *XLIFF Version 1.2*: https://docs.oasis-open.org/xliff/v1.2/os/xliff-core.html
