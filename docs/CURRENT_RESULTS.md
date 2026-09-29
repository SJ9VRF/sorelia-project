# SORELIA current evidence — v1.7.0

**Author:** Aura Yavary

This page is the canonical summary of the evidence that ships with the public research artifact. It deliberately separates engineering evidence from paper-scale scientific claims.

## Evidence tier

All committed numerical results are **engineering smoke evidence**. They establish that the system, controls, statistics, browser backend, and longitudinal failure-frontier instrumentation execute. They do **not** establish frontier-model superiority or production reliability.

## Retained engineering findings

- The real Chromium/Playwright fixture executes 12 isolated tasks and records failure/recovery trajectories. In the retained browser smoke, task success is 58.3%, with 54 recorded failure events and 27 recovery attempts.
- The local closed-loop smoke has produced runs where aggregate task success remained 90% while introduced frontier risk exceeded removed risk (`risk displacement ≈ 1.33×`). This is retained because it illustrates the motivating measurement problem; it is not a frontier-model result.
- Fixed-budget and repeated-trial toy comparisons include mixed, null, and adverse outcomes. SORELIA is **not** universally best in these local runs.
- Static-priority, shuffled-label, random-cluster, no-exploration, and single-iteration controls execute. Some controls outperform full SORELIA on toy metrics; these results are retained rather than tuned away.
- Local/reference policies report token/cost coverage as unavailable when usage is not measured. Unknown cost is `null`, not zero.

## What is actually validated

- executable local and Chromium environment paths
- trajectory/failure/recovery logging
- state-based grading
- failure clustering and stable cross-round mechanism matching
- extinction/emergence/expansion/contraction/persistence states
- split/merge topology events and risk displacement
- fixed verified-data budget comparisons
- repeated trials, bootstrap intervals, and paired randomization tests
- train/eval leakage gates and near-duplicate diagnostics
- negative controls
- provenance and benchmark split hashing
- claim-to-evidence auditing
- provider adapter parsing/usage accounting with injected offline clients

## Still required before scientific performance claims

- real trainable interactive VLM/LLM post-training
- independently authored browser/desktop benchmark tasks at meaningful scale
- held-out site/application-family generalization
- 5+ training seeds and repeated evaluation trials
- independent human mechanism-identity annotation/calibration
- full data-path ablations on real agents
- strong published-agent baselines under matched budgets

No SOTA, production-reliability, or proprietary-frontier-model performance claim should be made until those gates are complete.
