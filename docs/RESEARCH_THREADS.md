# Research Threads — hypothesis to rerun

This page is intentionally process-shaped rather than presentation-shaped. It shows how a research question changed after evidence pushed back.

## THREAD-001 — From scalar success to risk displacement

**Hypothesis / question**  
Task-success improvement is insufficient to characterize post-training reliability.

**Executed evidence**  
Experiments: EXP-003, EXP-004  
Raw artifacts: `artifacts/v110_smoke/metrics.json`, `artifacts/plots/v110_risk_displacement.png`, `artifacts/eval_runs/v100_compare.json`

**What broke / surprised us**  
F1

**Decision(s)**  
D1, D5

**Current conclusion**  
A policy update can preserve aggregate task success while introducing more frontier risk than it removes. This is engineering-smoke evidence, not a frontier-model result.

**Git-history boundary**  
The methodological changes predate the retained Git history boundary; current Evidence Layer commits preserve the surviving artifacts rather than reconstructing missing commits.

## THREAD-002 — Failure identity: coarse labels → optimal matching → ambiguity calibration

**Hypothesis / question**  
Longitudinal failure analysis requires mechanism identity that survives changing cluster IDs.

**Executed evidence**  
Experiments: EXP-009  
Raw artifacts: `artifacts/v110_smoke/frontier_i2.json`, `artifacts/v110_smoke/matching_annotation_packet_i2.jsonl`

**What broke / surprised us**  
F3, F4

**Decision(s)**  
D2, D8

**Current conclusion**  
Stable mechanism matching is necessary but not self-validating; ambiguous matches remain a human-calibration gate.

**Git-history boundary**  
No historical commit is claimed for the original coarse-label or greedy versions; the retained artifacts and decision record document the correction.

## THREAD-003 — Comparison integrity: mislabeled SORELIA arm → fixed-budget controlled benchmark

**Hypothesis / question**  
The moving-frontier scheduler should be compared under identical verified-data budgets.

**Executed evidence**  
Experiments: EXP-004, EXP-005  
Raw artifacts: `artifacts/eval_runs/v100_compare.json`, `artifacts/v100_compare.json.manifest.json`, `artifacts/v070_release_multiseed.json`

**What broke / surprised us**  
F5

**Decision(s)**  
D3, D5

**Current conclusion**  
The old comparison was invalid for attributing effects to SORELIA; regenerated comparisons enforce the actual frontier-aware path and equal verified-data budgets.

**Git-history boundary**  
The v0.5 bug predates retained Git history. Its existence is disclosed rather than backfilled with a fake commit.

## THREAD-004 — Usage accounting: synthetic precision → measured-or-null

**Hypothesis / question**  
Efficiency metrics are only meaningful when usage is measured rather than fabricated.

**Executed evidence**  
Experiments: EXP-002  
Raw artifacts: `artifacts/browser_smoke.json`, `artifacts/browser_smoke_stdout.txt`

**What broke / surprised us**  
F6

**Decision(s)**  
D6, D7

**Current conclusion**  
Unknown token/cost values remain null with explicit coverage; provider failures are separated from scientific agent failures.

**Git-history boundary**  
The correction predates retained Git history; current release contracts enforce the truthful accounting behavior.

