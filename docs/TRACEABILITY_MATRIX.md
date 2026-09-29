# Traceability Matrix

**Author:** Aura Yavary  
**Release:** v1.7.0

This matrix connects the polished research story to retained evidence. It deliberately distinguishes **archived evidence** from **retained Git history**. SORELIA does not reconstruct commits that were not preserved.

| Thread | Hypothesis / question | Experiments | Failed assumptions | Decisions | Raw evidence | Implementation / config | Current conclusion |
|---|---|---|---|---|---|---|---|
| THREAD-001: From scalar success to risk displacement | Task-success improvement is insufficient to characterize post-training reliability. | EXP-003, EXP-004 | F1 | D1, D5 | `artifacts/v110_smoke/metrics.json`<br>`artifacts/plots/v110_risk_displacement.png`<br>`artifacts/eval_runs/v100_compare.json` | `src/sorelia/evidence.py`<br>`src/sorelia/features.py`<br>`src/sorelia/pipeline.py`<br>`configs/release_gate.yaml` | A policy update can preserve aggregate task success while introducing more frontier risk than it removes. This is engineering-smoke evidence, not a frontier-model result. |
| THREAD-002: Failure identity: coarse labels → optimal matching → ambiguity calibration | Longitudinal failure analysis requires mechanism identity that survives changing cluster IDs. | EXP-009 | F3, F4 | D2, D8 | `artifacts/v110_smoke/frontier_i2.json`<br>`artifacts/v110_smoke/matching_annotation_packet_i2.jsonl` | `src/sorelia/evidence.py`<br>`src/sorelia/features.py`<br>`src/sorelia/schema.py`<br>`docs/HUMAN_CALIBRATION_PROTOCOL.md` | Stable mechanism matching is necessary but not self-validating; ambiguous matches remain a human-calibration gate. |
| THREAD-003: Comparison integrity: mislabeled SORELIA arm → fixed-budget controlled benchmark | The moving-frontier scheduler should be compared under identical verified-data budgets. | EXP-004, EXP-005 | F5 | D3, D5 | `artifacts/eval_runs/v100_compare.json`<br>`artifacts/v100_compare.json.manifest.json`<br>`artifacts/v070_release_multiseed.json` | `src/sorelia/experiments.py`<br>`src/sorelia/experiments_multiseed.py`<br>`tests/test_compare_contract.py`<br>`configs/release_gate.yaml` | The old comparison was invalid for attributing effects to SORELIA; regenerated comparisons enforce the actual frontier-aware path and equal verified-data budgets. |
| THREAD-004: Usage accounting: synthetic precision → measured-or-null | Efficiency metrics are only meaningful when usage is measured rather than fabricated. | EXP-002 | F6 | D6, D7 | `artifacts/browser_smoke.json`<br>`artifacts/browser_smoke_stdout.txt` | `src/sorelia/schema.py`<br>`src/sorelia/pipeline.py`<br>`tests/test_metrics_usage_unknown.py`<br>`docs/USAGE_ACCOUNTING.md` | Unknown token/cost values remain null with explicit coverage; provider failures are separated from scientific agent failures. |

## How to audit a thread

1. Read the experiment entry in `docs/EXPERIMENT_JOURNAL.md`.
2. Open the failed assumption in `docs/FAILED_EXPERIMENTS.md`.
3. Inspect the corresponding decision in `docs/DECISION_LOG.md`.
4. Verify the raw file hash in `docs/EVIDENCE_LEDGER.json`.
5. Check `docs/GIT_HISTORY.md` before attributing a historical code change to a retained commit.

## Important boundary

A raw artifact can support a historical result without proving that the exact historical source commit was retained. The release keeps those claims separate.
