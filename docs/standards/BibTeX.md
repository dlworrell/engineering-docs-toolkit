# BibTeX

## Purpose

BibTeX is a long-established bibliographic data format and processing system used with TeX and LaTeX. It separates bibliographic records from document text and identifies each record with a citation key.

BibTeX is best treated as a widely adopted interchange format and ecosystem convention rather than a complete modern metadata standard.

## Where EDT Uses BibTeX

- Import of existing `.bib` databases.
- Export for TeX and LaTeX workflows.
- Migration of legacy scholarly projects.
- Exchange with reference managers and publishing tools that support BibTeX.
- Preservation of citation keys used by source documents.

## Where EDT Does Not Use BibTeX

BibTeX is not EDT's canonical bibliographic model. Its entry types and fields are too limited and inconsistent to represent all contributor roles, identifiers, multilingual metadata, structured names, dates, and publication relationships required by EDOM.

BibTeX style files also do not replace CSL in EDT's publication architecture. EDT uses CSL for citation and bibliography presentation, while BibTeX remains primarily an import and export format.

## Mapping to EDOM

Representative BibTeX structures map approximately as follows:

| BibTeX | EDOM |
| --- | --- |
| Citation key | Stable local bibliography identifier |
| Entry type | Bibliographic resource type |
| `author` | Contributor list with author role |
| `editor` | Contributor list with editor role |
| `title` | Resource title |
| `journal` | Container title |
| `booktitle` | Parent publication title |
| `year`, `month` | Publication date |
| `volume`, `number`, `pages` | Publication details |
| `publisher` | Publisher metadata |
| `doi`, `isbn`, `url` | External identifiers and locators |
| `note` | Unstructured note |

Importers should preserve the original entry type, field names, citation key, field order where practical, and source location through provenance.

## Import Strategy

A BibTeX importer should:

1. Parse entries without silently discarding unknown fields.
2. Preserve citation keys exactly unless a profile explicitly normalizes them.
3. Normalize names, dates, identifiers, and page ranges into structured EDOM fields.
4. Retain original field values for round-trip and audit purposes.
5. Report malformed entries, duplicate keys, ambiguous names, and unsupported macros.
6. Distinguish standard BibTeX fields from tool-specific extensions.

Case-protection braces and TeX markup should be interpreted carefully. Their semantic intent should be preserved even when the target publication format is not TeX.

## Export Strategy

A BibTeX exporter should emit a declared compatibility profile, for example classic BibTeX or a documented extended field set.

Export should report:

- Metadata that cannot be represented faithfully.
- Contributor roles that must be flattened.
- Structured dates reduced to year or month fields.
- Identifiers or multilingual fields written through extensions.
- Character encoding or TeX-escaping decisions.

Round-trip preservation should be preferred when EDT imported the source from BibTeX and no semantic edits require a different representation.

## BibLaTeX and Biber

BibLaTeX and Biber support a richer data model than classic BibTeX, including broader entry types, contributor roles, date handling, localization, and Unicode-oriented workflows.

EDT should treat BibLaTeX data as a related but distinct import and export profile. It must not assume that every `.bib` file follows classic BibTeX semantics.

## Validation

EDT validation may include:

- Duplicate or missing citation keys.
- Missing required fields by resource type or project profile.
- Invalid DOI, ISBN, URL, or date syntax.
- Unresolved string macros or cross-references.
- Ambiguous author-name parsing.
- Citation targets absent from the bibliography.
- Fields that cannot be represented in the requested export profile.

## Design Notes

BibTeX remains important because of its installed base, portability, and broad tool support. EDT should bridge to it carefully without adopting its limitations as the internal bibliographic architecture.

The architectural boundary is:

```text
EDOM owns normalized bibliographic meaning.
BibTeX provides legacy and ecosystem interchange.
CSL controls citation presentation.
```

## References

- Oren Patashnik, *BibTeXing*: https://mirrors.ctan.org/biblio/bibtex/base/btxdoc.pdf
- CTAN, BibTeX package information: https://ctan.org/pkg/bibtex
