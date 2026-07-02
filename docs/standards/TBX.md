# TBX

TBX (TermBase eXchange) is an XML standard for exchanging structured terminology data.

EDT targets ISO 30042:2019 for production interchange and classifies TBX as **Adopt** for terminology exchange and **Bridge** for terminology-management systems.

## Architectural Boundary

```text
EDOM owns document semantics and term occurrences.
TBX exchanges concept-oriented terminology records.
SKOS may own taxonomy and concept-scheme relationships.
```

## Core Model

TBX is concept-oriented. A concept entry may contain several language sections, and each language section may contain several terms.

| TBX concept | EDT meaning |
| --- | --- |
| Concept entry | Stable terminology concept |
| Language section | Language-specific concept view |
| Term section | One term or designation |
| Definition | Concept definition |
| Context | Usage evidence |
| Subject field | Domain classification |
| Term status | Preferred, admitted, or deprecated status |
| Cross-reference | Relationship to another concept or resource |

EDT must preserve the distinction between a concept, a language-specific term, and a term occurrence in a document.

## Import and Export

Importers should preserve identifiers, language tags, terms, definitions, contexts, sources, status, data-category identifiers, extensions, and source provenance.

Exporters should declare the TBX profile, preserve concept-oriented organization, emit only supported data categories, validate the result, and report information that cannot be represented faithfully.

## Validation

EDT validation may include:

- XML or schema errors.
- Unsupported TBX profile.
- Missing or duplicate identifiers.
- Missing language sections or terms.
- Multiple preferred terms where prohibited.
- Deprecated terms used in publication content.
- Unknown data categories.
- Broken references.
- Missing definitions or sources required by profile.

Schema validity alone does not prove that a termbase is editorially coherent.

## Relationship to Other Standards

- TBX manages concepts and terms.
- SKOS manages concept schemes and semantic relationships.
- XLIFF applies terminology during localization jobs.
- TMX stores reusable translated segments.
- EDOM records terminology occurrences in documents.

## Design Rule

```text
Model concepts separately from terms.
Preserve language, status, and provenance.
Treat terminology as governed semantic data, not a flat word list.
```
