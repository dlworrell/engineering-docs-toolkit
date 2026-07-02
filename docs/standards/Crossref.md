# Crossref

## Purpose

Crossref provides infrastructure for registering and connecting scholarly metadata through Digital Object Identifiers (DOIs). Its metadata ecosystem supports persistent identification, citation linking, funding information, licenses, references, relationships, corrections, retractions, and discovery.

Crossref is not a document-authoring vocabulary. It is a registration and metadata-interchange system for scholarly objects.

## Current Standard

EDT should target the latest Crossref metadata deposit schema supported by the selected publication profile. As of September 2025, Crossref recommends metadata deposit schema version 5.4.0.

The schema version, deposit type, account, DOI prefix, and submission result must be recorded in publication provenance.

## Where EDT Uses Crossref

- Preparing DOI registration metadata.
- Registering journal articles, books, chapters, conference papers, datasets, reports, standards, dissertations, grants, peer reviews, posted content, and related scholarly objects.
- Depositing references and relationship metadata.
- Recording funders, licenses, contributors, identifiers, and publication dates.
- Retrieving and reconciling existing scholarly metadata.
- Verifying DOI records after registration or update.
- Supporting citation linking and correction/retraction workflows.

## Where EDT Does Not Use Crossref

Crossref is not EDT's canonical document model and does not contain the full semantic content of a document. EDOM remains authoritative for document structure, equations, figures, tables, prose, source regions, validation state, provenance, and internal reference relationships.

Crossref metadata should also not be treated as automatically correct merely because a record exists. Imported records require validation and reconciliation against authoritative project sources.

## Mapping to EDOM

Representative Crossref metadata maps approximately as follows:

| Crossref | EDOM |
| --- | --- |
| DOI | Persistent external identifier |
| Title and subtitle | Document title metadata |
| Contributor | Structured contributor and role metadata |
| ORCID | Contributor identifier |
| Publication dates | Date metadata with declared semantics |
| Container title | Parent publication metadata |
| ISBN / ISSN | Publication identifiers |
| Publisher | Publisher metadata |
| Abstract | Abstract node or metadata |
| References | Bibliographic entries and citation relationships |
| Relations | Typed reference-graph edges |
| Funding data | Funder and award metadata |
| License | Rights and license metadata |
| Resource URL | Published landing-page locator |
| Crossmark update | Version, correction, or retraction relationship |

EDOM may contain information richer than Crossref supports. Export must report any information that cannot be deposited.

## Deposit Strategy

A Crossref publication stage should:

1. Validate the EDOM document and publication profile.
2. Confirm that the DOI, landing-page URL, title, contributors, dates, and publication relationships are complete.
3. Select a declared Crossref schema version and record type.
4. Generate XML that validates against the corresponding Crossref schema.
5. Submit through an approved registration workflow.
6. Capture the submission identifier and complete submission log.
7. Verify the registered metadata after processing.
8. Preserve the generated XML and returned status as provenance artifacts.

A successful HTTP request does not by itself prove successful registration. Submission logs and the resulting record must be checked.

## Updates and Corrections

Crossref records are maintained over time. EDT should support deliberate metadata updates while preserving the history of what changed, why it changed, and which source justified the change.

Corrections, retractions, replacements, translations, supplements, and other relationships should be represented semantically in EDOM before Crossref deposit. Publisher-specific profiles may impose additional requirements for Crossmark or update policies.

## Retrieval Strategy

EDT may retrieve Crossref metadata through supported APIs or content-negotiation mechanisms for:

- DOI resolution and enrichment.
- Bibliographic reconciliation.
- Reference matching.
- Validation of publication metadata.
- Detection of corrections, retractions, or related works.

Retrieved metadata must record its access time, request parameters, source endpoint, and returned identifier. External metadata should not silently overwrite curated EDOM values.

## Validation

EDT validation may include:

- DOI syntax and prefix policy.
- Missing or duplicate identifiers.
- Missing landing-page URLs.
- Incomplete contributor metadata.
- Invalid or ambiguous publication dates.
- Inconsistent container, ISBN, or ISSN metadata.
- Missing references required by a profile.
- Unresolved relationship targets.
- Crossref schema-validation failures.
- Submission or registration errors.
- Differences between the intended deposit and retrieved record.

## Profiles

An EDT Crossref profile may specify:

- Record type.
- Deposit schema version.
- Required and recommended fields.
- DOI construction policy.
- Contributor and ORCID requirements.
- Reference-deposit policy.
- Funding and license requirements.
- Relationship metadata rules.
- Crossmark requirements.
- Deposit endpoint and verification procedure.

Profiles must distinguish EDT semantic validation from Crossref schema validity and business-rule compliance.

## Design Notes

Crossref should be treated as a first-class scholarly metadata bridge, not as an internal authoring format. EDT owns the complete semantic and provenance-rich document model; Crossref provides persistent identifiers and interoperable registration metadata for published scholarly objects.

The architectural boundary is:

```text
EDOM owns the scholarly object's full semantic meaning.
Crossref receives the publication metadata required to identify and connect it.
```

## References

- Crossref, *Schema library*: https://www.crossref.org/documentation/schema-library/
- Crossref, *Metadata deposit schema 5.4.0*: https://data.crossref.org/reports/help/schema_doc/5.4.0/index.html
- Crossref, *REST API documentation*: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
