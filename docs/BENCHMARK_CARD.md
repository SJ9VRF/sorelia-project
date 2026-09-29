# SORELIA benchmark card

## Purpose

The bundled benchmark is an **engineering harness**, not a claim of ecological coverage of real-world computer use. It exists to test failure discovery, longitudinal mechanism tracking, fixed-budget curricula, recovery logging, contamination controls, and statistical instrumentation.

## Task families

The local generator covers browser, document, spreadsheet, email-like, file-management, and multi-application abstractions. The Chromium fixture provides a real DOM/action loop in an isolated local page.

## Splits

Every run writes `benchmark_manifest.json` with task IDs, seeds, family metadata, fingerprints, and split SHA-256 digests for train/eval/stress sets.

## Stress split

The stress split increases difficulty/horizon/perturbation and changes task ordering. It is a deterministic distribution-shift probe—not a substitute for held-out real websites or desktop applications.

## Grading

Core outcomes are state-based. Model-based grading is not required for the bundled smoke benchmark.

## Leakage policy

Exact task-ID/fingerprint leakage is a hard failure. Near-duplicate diagnostics are reported separately. See `docs/CONTAMINATION_PROTOCOL.md`.

## Known limitations

- synthetic/local task distribution;
- limited UI diversity;
- no claim of production representativeness;
- no human-calibrated mechanism identity in the public engineering release;
- no frontier-agent superiority result.
