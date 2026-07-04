# P1 HERKULES Acceptance Harness

Date: 2026-07-03

## Purpose

P1 begins real integration pressure against HERKULES.

P0 proved that the initialized EDT product path is truthful and failure-aware. P1 now uses HERKULES as the acceptance corpus to expose real importer, EDOM, validation, reference, report, and publishing failures.

The first P1 harness is intentionally opt-in. It does not require the HERKULES source PDF to be committed to this repository. That keeps normal CI stable while allowing local or protected CI jobs to run the real acceptance corpus.

## Acceptance test

The HERKULES acceptance test is located at:

```text
tests/acceptance/test_herkules_acceptance.py
```

It runs the user-facing CLI path:

```text
edt init
  -> configure HERKULES source
  -> edt import
  -> edt build
  -> edt check
```

When a HERKULES source PDF is present, the test asserts that:

- the import report exists
- canonical EDOM exists
- the build manifest exists
- validation, reference graph, and quality reports exist
- the source is recorded as present
- the import status is `imported`
- canonical EDOM contains at least one imported page
- the build source mode is `canonical-edom`
- document reports are attached to the build manifest
- `edt check` exits successfully
- the quality report marks the document as publication-ready

## Running the harness

Set the source PDF path and run the acceptance test:

```bash
EDT_HERKULES_SOURCE_PDF=/path/to/herkules-manual.pdf \
python -m pytest tests/acceptance/test_herkules_acceptance.py
```

Optional page controls:

```bash
EDT_HERKULES_FIRST_PAGE=1
EDT_HERKULES_LAST_PAGE=1
```

Optional OCR control:

```bash
EDT_HERKULES_OCR_ENGINE=tesseract
```

If `EDT_HERKULES_SOURCE_PDF` is not set and no local fixture exists at `tests/acceptance/fixtures/herkules-manual.pdf`, the test skips.

## Expected P1 behavior

A failing HERKULES acceptance run should not be treated as a P0 regression unless it breaks the product-path guarantees closed in P0.

Most failures should become P1 findings, categorized by subsystem:

- importer
- PDF/page extraction
- OCR
- layout analysis
- semantic recognition
- EDOM assembly
- validation
- reference graph
- quality scoring
- publishing/export
- CLI/check truthfulness

The point of P1 is to turn real HERKULES failures into specific engineering tasks.

## Next steps

1. Run the harness against the real HERKULES source PDF.
2. Record the first failure exactly.
3. Convert that failure into the smallest useful P1 issue or commit.
4. Add expected artifact snapshots only after the first stable HERKULES pass exists.
5. Keep broad importer rewrites out of P1 until the acceptance harness identifies concrete failures.
