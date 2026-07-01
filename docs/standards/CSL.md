# Citation Style Language (CSL)

## Purpose

Citation Style Language (CSL) is an open XML vocabulary for defining how citations and bibliographies are formatted. It separates bibliographic data from presentation rules so the same references can be rendered in different journal, publisher, disciplinary, or institutional styles.

## Current Standard

EDT should target CSL 1.0.2 unless a project profile explicitly requires another version for compatibility or archival reproducibility.

The selected CSL style, locale, processor, and version should be recorded in project configuration and publication provenance.

## Where EDT Uses CSL

- Formatting in-text citations.
- Formatting notes and bibliographies.
- Applying journal- or publisher-specific reference styles.
- Reusing the same bibliographic data across publication targets.
- Supporting profile-specific citation policies.
- Reproducible citation rendering.

## Where EDT Does Not Use CSL

CSL is not EDT's canonical bibliographic data model and does not define the semantic structure of the surrounding document. EDOM remains responsible for citation nodes, bibliography entries, identifiers, reference relationships, provenance, and validation.

CSL controls presentation. It should not be treated as the source of truth for authorship, titles, dates, identifiers, or publication metadata.

## Mapping to EDOM

EDOM citation and bibliography structures map to CSL processing approximately as follows:

| EDT / EDOM | CSL role |
| --- | --- |
| Citation node | Citation request supplied to a CSL processor |
| Bibliography entry | Bibliographic item data |
| Citation cluster | Ordered group of citation items |
| Locator | Page, chapter, section, figure, or other locator |
| Prefix / suffix | Citation-affix data |
| Author and editor metadata | CSL name variables |
| Title and container metadata | CSL title variables |
| Dates | CSL date variables |
| DOI, ISBN, URL, and other identifiers | CSL identifier variables where supported |
| Publication profile | Selected CSL style and locale policy |

The rendered citation text is publication output. The underlying EDOM citation relationship and bibliographic metadata remain authoritative.

## Processing Strategy

A CSL publication stage should:

1. Validate citation targets and bibliography identifiers before rendering.
2. Convert EDOM bibliographic metadata into the selected processor's CSL-compatible data form.
3. Apply a declared CSL style and locale.
4. Preserve citation order, locators, prefixes, suffixes, and suppress-author behavior.
5. Record the processor, style identifier, style revision, locale, and CSL version used.
6. Produce deterministic output for the same semantic input and configuration.

## Validation

EDT validation should distinguish between bibliographic correctness and citation formatting.

Semantic validation may include:

- Missing citation targets.
- Duplicate bibliography identifiers.
- Unused bibliography entries.
- Missing required authors, titles, dates, or identifiers.
- Invalid locator types.
- Profile-specific reference requirements.

CSL processor errors and unavailable style dependencies should be reported separately as publication failures.

## Profiles and Local Styles

EDT profiles may select or constrain:

- The required CSL style.
- Allowed style variants.
- Locale behavior.
- Note versus author-date citation systems.
- Required bibliographic fields.
- Identifier and URL presentation rules.
- Publisher-specific local style files.

Local or modified styles should carry stable identifiers, revision history, licensing information, and provenance. Silent modification of an upstream style should be avoided.

## Import and Export

EDT may import citation metadata from formats such as BibTeX, CSL-JSON, JATS, TEI, DocBook, or other structured sources. Importers should normalize the data into EDOM while preserving the source representation and identifiers.

EDT may export bibliographic data separately from rendered citations. Exporting both the normalized data and the selected CSL style improves reproducibility.

## Design Notes

CSL provides mature prior art for separating citation semantics from citation presentation. EDT should adopt CSL for formatting rather than implementing proprietary journal-style logic in publishers.

The key architectural boundary is:

```text
EDOM owns citation meaning and reference relationships.
CSL owns citation and bibliography presentation.
```

## References

- Citation Style Language project: https://citationstyles.org/
- CSL 1.0.2 specification: https://docs.citationstyles.org/en/stable/specification.html
- CSL styles repository: https://github.com/citation-style-language/styles
