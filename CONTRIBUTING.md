# Contributing to SORELIA

SORELIA is a research prototype. Contributions should improve scientific validity, reproducibility, safety, or implementation quality—not merely increase headline metrics.

## Before opening a PR

1. Read `docs/TRUTH_AUDIT.md`, `docs/CLAIM_EVIDENCE_REGISTRY.json`, and `docs/REVIEWER_REPRODUCTION.md`.
2. Run `pytest -q`, `sorelia audit --root .`, and `sorelia doctor`.
3. If an experiment changes a public claim, regenerate its evidence artifact and update the claim/evidence registry.
4. Keep null and adverse results. Do not remove them because they weaken the narrative.
5. Never convert unknown token usage, cost, or latency into zero-valued measurements.

## Research changes

A research-method PR should state:
- hypothesis or failure mode being tested;
- baseline(s) and fixed-budget constraint;
- train/eval split impact;
- contamination risk;
- expected falsification condition;
- exact artifact(s) regenerated.

## Code changes

- Keep the provider boundary isolated from evaluation logic.
- Do not classify SDK/network/parser failures as agent failures.
- Preserve deterministic seeds where applicable.
- Add regression tests for corrected methodological bugs.

## Evidence tiers

Engineering smoke evidence validates execution, not frontier-model superiority. Paper-scale claims require the gates in `docs/PAPER_READINESS.md`.
