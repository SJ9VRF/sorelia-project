# Reviewer-facing quality checklist

## Scientific validity
- [x] Main hypothesis is falsifiable.
- [x] Equal-budget baselines are implemented.
- [x] Held-out eval data is separated from curriculum construction.
- [x] Negative controls are specified.
- [x] Ablations are pre-specified.
- [x] Smoke-test results are explicitly separated from paper claims.
- [ ] Real browser/desktop experiments complete.
- [ ] Multiple model/training seeds complete.
- [ ] Confidence intervals and paired statistical tests complete.
- [ ] Human calibration complete. (v0.9 packet/scorer implemented; actual independent annotations pending.)

## Reproducibility
- [x] Config-driven execution.
- [x] Explicit seeds.
- [x] Raw traces retained.
- [x] Task verification before training.
- [x] Automated tests.
- [x] Provenance design documented.
- [ ] Production environment images/checkpoints pinned.

## Agent-eval quality
- [x] State-based task verification in local environment.
- [x] Full trajectory traces, not only final success.
- [x] Failure mechanism and recovery fields.
- [x] Cost/latency/step metrics.
- [ ] Human audit of real traces.
- [ ] Model-grader calibration where subjective grading is required.

## Safety
- [x] Catastrophic action metric.
- [x] Sandbox-only recommendation for high-risk actions.
- [x] Reward-hacking tests planned.
- [x] No claims based on live external accounts.

- [x] Exact train/eval semantic leakage gate executes.
- [x] Shuffled-label and random-cluster negative controls execute.
- [x] Blank human matching-calibration packet and agreement scorer execute.
