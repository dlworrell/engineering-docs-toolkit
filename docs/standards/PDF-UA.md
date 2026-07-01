# PDF/UA

## Purpose

PDF/UA (ISO 14289) defines how PDF documents are made universally accessible. It builds on the PDF specification by requiring semantic tagging, logical reading order, alternative text, navigational structures, and other accessibility features.

## Where EDT Uses PDF/UA

- Accessible PDF publication.
- Validation targets for exported PDFs.
- Logical document structure.
- Tagged figures, tables, and headings.
- Screen-reader compatibility.

## Where EDT Does Not Use PDF/UA

PDF/UA is an output standard, not EDT's internal semantic representation. EDOM retains the canonical semantic structure from which accessible PDFs are produced.

## Mapping to EDOM

EDOM provides the semantic hierarchy required to generate tagged PDFs. Headings, paragraphs, figures, captions, tables, equations, references, and accessibility metadata are translated into PDF/UA-compliant structures during publication.

## Design Notes

EDT's goal is to generate accessible PDFs from validated semantic content rather than attempting to infer accessibility during export. Accessibility should be established in EDOM and preserved through every publication target.