# Engineering Documents Toolkit (EDT)
## Project Charter

**Subtitle:** A Semantic Document Engineering Platform

**Status:** Draft for EDT 1.0

## Mission

The Engineering Documents Toolkit (EDT) exists to preserve the meaning of technical documents independently of their presentation.

EDT imports documents from diverse formats, normalizes them into the Engineering Document Object Model (EDOM), validates their structural and semantic integrity, preserves provenance throughout processing, and publishes consistent outputs from a single canonical representation.

## Vision

To create an open, standards-based semantic document engineering platform capable of preserving, validating, transforming, translating, publishing, and archiving technical knowledge across generations of software and publication technologies.

## Purpose

EDT provides:

- Multi-format document import
- Layout analysis
- Semantic recognition
- Engineering Document Object Model (EDOM)
- Provenance preservation
- Structural, semantic, and reference validation
- Reference graph generation
- Quality reporting
- Translation memory integration
- Multi-format publishing

EDT is not a word processor, desktop publishing application, or PDF editor. Its purpose is to understand documents, not merely render them.

## Engineering Principles

1. Semantics before presentation.
2. Preserve provenance at every stage.
3. Normalize once, publish many.
4. Validation operates on semantics.
5. Documents are knowledge, not pages.
6. Prefer open standards whenever practical.
7. Profiles extend the platform without modifying its core.

## Scope

EDT is responsible for importing, recognizing, normalizing, validating, enriching, publishing, and assessing the quality of technical documents.

## Non-Goals

EDT does not replace Microsoft Word, LibreOffice, LaTeX, Adobe InDesign, or PDF editors. Those tools create documents; EDT understands, validates, and publishes them.

## Relationship to Catalyst

Within the Catalyst ecosystem:

- AES defines engineering doctrine.
- AEMS evaluates engineering compliance.
- EDT provides semantic document engineering.
- HERKULES serves as the flagship demonstration and regression corpus.

Each repository has one primary responsibility.

## Long-Term Direction

EDT will evolve through standards adoption, profile-driven semantics, provenance preservation, reproducible publishing, and long-term knowledge preservation while maintaining a stable semantic core.