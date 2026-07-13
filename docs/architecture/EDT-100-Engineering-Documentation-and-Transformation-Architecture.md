---
id: EDT-100
title: Engineering Documentation and Transformation Architecture
status: draft
lifecycle: proposed
type: architecture
owner: EDT
version: 0.1.0
---

# EDT-100 — Engineering Documentation and Transformation Architecture

## 1. Purpose

This document defines EDT as the semantic documentation and report-production layer for the Catalyst ecosystem.

EDT extracts technical source material, preserves provenance, normalizes content into canonical semantic models, validates structure and references, transforms canonical data, and renders durable knowledge products. EDT does not make governance, compliance, remediation, or certification decisions.

## 2. Ecosystem responsibilities

### 2.1 AES

AES defines engineering obligations, evidence semantics, report semantics, and documentation standards.

### 2.2 AEMS

AEMS selects and enforces policy, orchestrates assessments, and aggregates repository-level results.

### 2.3 Project Zero

Project Zero executes repository initiation and remediation lifecycles: inspect, assess, plan, remediate, verify, and certify.

### 2.4 EDT

EDT owns:

- extraction adapters;
- source normalization;
- the Engineering Document Object Model (EDOM);
- canonical report and evidence ingestion interfaces;
- provenance-preserving transformations;
- validation of document structure and references;
- rendering profiles and publication outputs;
- document comparison and historical transformation products.

EDT does not own:

- assessment policy;
- finding severity decisions;
- repository readiness decisions;
- certification authority;
- project-specific source truth.

## 3. Architectural principle

Facts, evidence, and decisions shall exist once in canonical structured form. Output documents are reproducible projections of those canonical objects.

```text
Source material and repository evidence
                ↓
         Extraction adapters
                ↓
       Canonical semantic objects
                ↓
      Validation and relationship graph
                ↓
    Assessment decisions from P0/AEMS
                ↓
       Canonical report package
                ↓
          EDT rendering profiles
     ├── Markdown
     ├── JSON
     ├── HTML
     ├── PDF
     ├── EPUB
     ├── SARIF
     ├── CSV
     └── project-specific publications
```

## 4. Processing stages

### 4.1 Acquire

EDT receives authorized source material through adapters. Sources may include:

- repository files and Git history;
- workflow logs and artifacts;
- test, coverage, benchmark, and simulation results;
- Markdown, HTML, PDF, office documents, images, and scanned documents;
- specifications, ADRs, manuals, books, and research papers;
- Project Zero and AEMS report objects;
- issue, pull-request, review, and release records;
- external references and standards.

Acquisition records source authority, immutable revision where possible, media type, size, hash, collection time, and access limitations.

### 4.2 Extract

Extraction converts source representations into recoverable content units while retaining mappings to the original source.

Extraction adapters may perform:

- text and metadata extraction;
- OCR;
- page and coordinate mapping;
- table, figure, equation, and caption detection;
- heading and section recognition;
- code-block and register-table recognition;
- reference and citation discovery;
- repository and workflow inventory extraction.

Extraction shall identify lossy operations and confidence values where applicable.

### 4.3 Normalize

Extracted material is normalized into canonical semantic objects.

EDOM remains the canonical document model for authored and imported technical documents. Additional canonical objects may include:

- Evidence Object;
- Engineering Report Object;
- Finding Object;
- Traceability Edge;
- Publication Manifest;
- Transformation Record.

Normalization shall preserve identifiers, source mappings, language, units, equations, references, accessibility data, and provenance.

### 4.4 Validate

Validation operates at multiple levels:

- schema validity;
- structural integrity;
- semantic consistency;
- reference resolution;
- caption and figure integrity;
- equation numbering and cross-reference integrity;
- accessibility requirements;
- provenance completeness;
- report-required-field completeness;
- output-profile prerequisites.

Validation failures shall not silently discard content. EDT shall produce diagnostics and the largest truthful partial output allowed by the selected policy.

### 4.5 Relate

EDT constructs relationship graphs among documents, sections, evidence, findings, requirements, implementation artifacts, verification results, and decisions.

Required relationship support includes:

- cites;
- references;
- implements;
- verified_by;
- derived_from;
- supersedes;
- duplicates;
- supports_finding;
- supports_decision;
- canonical_owner.

### 4.6 Transform

Transformations consume canonical objects and produce canonical derived objects or rendered products.

Examples include:

- translation;
- summarization;
- index and concordance generation;
- glossary generation;
- traceability matrix generation;
- report comparison;
- release-note generation;
- book assembly;
- register-reference generation;
- certification-package assembly;
- archival normalization.

Every transformation shall produce a provenance record identifying inputs, tool and version, profile, configuration, output hash, warnings, and lossy behavior.

### 4.7 Render and publish

Renderers produce format-specific outputs from canonical models. Rendering profiles define presentation, required sections, styling, pagination, navigation, accessibility, and publication metadata.

Renderers shall not alter assessment results, severity, evidence identity, or certification decisions.

## 5. Canonical workspace

A standard EDT workspace may use:

```text
.edt/
├── manifests/
│   ├── acquisition.json
│   ├── extraction.json
│   └── publication.json
├── corpus/
│   ├── documents/
│   ├── reports/
│   ├── evidence/
│   ├── findings/
│   └── relationships/
├── provenance/
│   ├── sources.json
│   ├── transformations.json
│   └── checksums.sha256
├── cache/
└── outputs/
```

This is a logical architecture. Projects may relocate generated and cached data, provided the manifest records the locations and canonical ownership.

## 6. Project Zero integration

A Project Zero workflow should integrate EDT through three explicit contracts:

```text
edt extract → project-zero assess → edt render
```

### 6.1 Extraction contract

EDT supplies normalized repository and evidence objects to Project Zero. Project Zero shall not require EDT to decide whether an observed condition violates policy.

### 6.2 Assessment contract

Project Zero and AEMS produce findings, decisions, remediation records, and canonical Engineering Report objects conforming to AES standards.

### 6.3 Rendering contract

EDT consumes the canonical report package and renders selected outputs. Failure to render one format shall not invalidate the canonical assessment object or successful outputs in other formats.

## 7. Report production

For Project Zero and AEMS, EDT shall support profiles for:

- GitHub workflow summary;
- repository Markdown report;
- machine-readable JSON package;
- archival PDF;
- HTML dashboard;
- SARIF findings;
- CSV traceability and inventory matrices;
- certification package;
- historical comparison report.

The canonical report model remains format-neutral. A report fact shall not be independently recomputed by each renderer.

## 8. Documentation production

EDT also supports governed technical documentation beyond assessments:

- architecture handbooks;
- specifications;
- API and ABI references;
- hardware register manuals;
- verification and validation reports;
- operations manuals;
- translated manuals;
- books and Bentley-style build books;
- indexes, concordances, glossaries, and reference graphs.

Repositories own their source documents and publication policy. EDT owns reusable transformation and rendering mechanics.

## 9. Profiles and plugins

Profiles declare expected semantic rules and publication behavior for repository and document classes, including:

- general engineering;
- operating system and kernel;
- compiler and toolchain;
- FPGA and HDL;
- hardware;
- library and API;
- book and manual;
- research;
- translation;
- certification report.

Plugins may add importers, validators, recognizers, transformations, and renderers. Plugins shall declare dependencies, supported schema versions, deterministic behavior, security boundaries, and provenance behavior.

## 10. Incremental and reproducible builds

EDT shall support dependency-aware incremental builds. Dirty-state calculation shall include:

- source hashes;
- canonical object hashes;
- profile versions;
- plugin versions;
- renderer versions;
- transformation configuration;
- dependencies and relationship edges.

A publication is reproducible when the same canonical inputs, declared tools, versions, profiles, and configuration produce semantically equivalent output. Byte-for-byte reproducibility may be required by a profile.

## 11. Historical comparison

EDT shall support comparison of successive canonical report and document states. Comparison products may include:

- added, removed, changed, and moved sections;
- new, resolved, reopened, and reclassified findings;
- changed evidence and provenance;
- reference-graph changes;
- metric and certification trends;
- translation-memory and terminology changes.

Comparison shall distinguish source changes from profile, policy, or renderer changes.

## 12. Security and trust boundaries

EDT processes potentially hostile and malformed input. Importers and plugins shall treat all external content as untrusted.

The architecture shall support:

- sandboxed or isolated importers where practical;
- bounded resource use;
- no implicit execution of embedded code or macros;
- path traversal prevention;
- safe archive handling;
- controlled network access;
- secret and personal-data detection or redaction policy;
- plugin trust and version records;
- deterministic failure diagnostics.

## 13. Failure behavior

EDT shall distinguish:

- acquisition failure;
- extraction failure;
- normalization failure;
- validation failure;
- transformation failure;
- rendering failure;
- publication failure.

A failure record shall identify the stage, source or object, diagnostic, tool version, and recoverability. Partial results shall be clearly marked and shall not be presented as complete.

## 14. Initial implementation priorities

1. Define canonical Evidence and Engineering Report ingestion schemas aligned with CAN-120 and CAN-130.
2. Add a Project Zero report rendering profile for Markdown and JSON.
3. Add provenance-preserving archival PDF rendering.
4. Add historical report comparison.
5. Expose the pipeline through a reusable CLI and GitHub Actions workflow.
6. Preserve current EDOM compatibility and existing document publishing behavior.

## 15. Acceptance criteria

EDT conforms to this architecture when it:

1. separates source acquisition, extraction, canonical modeling, validation, transformation, and rendering;
2. preserves provenance from source to every derived product;
3. consumes assessment decisions without becoming the assessment authority;
4. renders the same canonical report into at least JSON and Markdown;
5. records profile, tool, and plugin versions;
6. identifies lossy transformations and partial outputs;
7. supports reusable workflows for Project Zero, AEMS, and project repositories;
8. supports deterministic comparison of successive document or report states.
