# Experiment Matrix

**Author:** Aura Yavary

All rows below correspond to retained experiment evidence in this repository. These are engineering/methodology experiments, not frontier-model benchmark claims.

| ID | Experiment | Hypothesis | Retained result | Interpretation / next decision | Primary evidence |
|---|---|---|---|---|---|
| EXP-001 | Local closed-loop smoke | Can collect→cluster→allocate→verify→train→reevaluate execute end-to-end? | Loop emitted trajectories, clusters, allocations, verified tasks, corrections, metrics, manifests. | Aggregate success alone was insufficient; add longitudinal failure-frontier instrumentation. | `executed/exp-001-local-closed-loop-smoke.md` |
| EXP-002 | Chromium browser fixture | Does the environment abstraction survive a real browser DOM/action loop? | 58.3% success across 12 fixture tasks; 54 failure events; 27 recovery attempts; attempted recoveries succeeded. | Browser path is real engineering evidence but too narrow for computer-use scientific claims. | `executed/exp-002-chromium-browser-fixture.md`, `results/browser_smoke.json` |
| EXP-003 | Moving failure-frontier smoke | Can task success stay flat while reliability risk shifts adversely? | Success stayed 0.90 while risk introduced 0.5949 exceeded risk removed 0.4485; displacement 1.3263×. | Promote risk displacement and mechanism transitions to core outputs. | `executed/exp-003-moving-failure-frontier-smoke.md`, `../artifacts/v110_smoke/metrics.json` |
| EXP-004 | Fixed-budget curriculum comparison | Does frontier-aware allocation dominate simpler curricula under equal verified-data budgets? | In retained v0.8 smoke SORELIA did **not** win; human-balanced led IID, frequency led stress. | Keep strong simple baselines and block superiority claims pending real-agent evidence. | `executed/exp-004-fixed-budget-curriculum-comparison.md`, `results/v100_compare.json` |
| EXP-005 | Repeated-trial / multiseed inference | Are apparent differences stable under repeated stochastic evaluation? | Mixed effects; retained intervals often included zero; no stable advantage established. | Single-draw agent evaluation is too brittle; require repeated trials + paired inference. | `executed/exp-005-repeated-trial---multiseed-inference.md`, `results/v070_release_multiseed.json` |
| EXP-006 | Shifted stress split | Do conclusions survive a harder/longer deterministic shift? | Method ordering changed between IID and stress metrics. | Keep stress metrics separate; do not call this real website-family OOD. | `executed/exp-006-shifted-stress-split.md` |
| EXP-007 | Exploration ablation | Does an exploration reserve reliably help? | Removing exploration sometimes improved IID success. | Treat exploration ratio as empirical; do not assume monotonic benefit. | `executed/exp-007-exploration-ablation.md`, `results/v100_ablations.json` |
| EXP-008 | Semantic negative controls | Does the method depend on meaningful failure semantics? | Random clusters/static priority were competitive or better in toy smoke. | Toy harness cannot establish causal value of semantic mechanism tracking; keep negative controls mandatory. | `executed/exp-008-semantic-negative-controls.md`, `results/v100_ablations.json` |
| EXP-009 | Matching ambiguity audit | Are cross-round mechanism identities certain enough to treat as ground truth? | A retained run had 25% ambiguous matches; another example had 50% among matched mechanisms. | Automatic identity is not ground truth; require human calibration before validated-identity claims. | `executed/exp-009-matching-ambiguity-audit.md` |

## Reading rule

A method being present in this table does **not** imply it outperformed baselines. Null and adverse outcomes are intentionally retained.
