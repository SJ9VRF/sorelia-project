# SORELIA Experiments Workspace

**Author:** Aura Yavary  
**Release:** v1.7.0 corrected packaging

This directory is the experiment-facing entry point for SORELIA. It is intentionally populated with the retained experiment record rather than being an empty placeholder.

## What is here

- `EXPERIMENT_MATRIX.md` — one-screen map of the executed experiment families, hypotheses, outcomes, and next decisions.
- `RUN_INDEX.json` — machine-readable registry of the retained experiment families and their evidence paths.
- `executed/` — the nine retained experiment logs. Each log has **Hypothesis → Setup → Result → Interpretation → Next decision**.
- `configs/` — copies of the actual retained experiment configurations used by the released smoke/release harnesses.
- `results/` — retained comparison, ablation, multiseed, browser, and release-result artifacts.
- `raw/README.md` — where the deeper trajectory/frontier/allocation artifacts live in the repository and how to follow them.
- `paper_scale/PENDING_EXPERIMENTS.md` — experiments required before scientific/SOTA claims are allowed.

## Evidence boundary

The retained experiments are **engineering smoke / methodology evidence**, not frontier-model performance evidence. Several results are null or adverse. They are kept deliberately because the purpose of this workspace is to show what actually happened, not to create a success-only narrative.

For the full research process, also see:

- `../docs/EXPERIMENT_JOURNAL.md`
- `../docs/FAILED_EXPERIMENTS.md`
- `../docs/DECISION_LOG.md`
- `../docs/UNEXPECTED_FINDINGS.md`
- `../docs/TRACEABILITY_MATRIX.md`
- `../docs/EVIDENCE_LEDGER.json`
- `../artifacts/`
