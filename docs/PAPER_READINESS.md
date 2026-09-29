# Paper-readiness checklist

A submission-quality SORELIA result requires four independent forms of evidence.

**Causal curriculum evidence.** Equal-budget random, difficulty, human-balanced, frequency-only, static-failure, and adaptive curricula; shuffled-label and random-cluster controls; matched optimizer/model/data budgets; repeated seeds.

**Generalization evidence.** Held-out task instances, surface perturbations, failure variants, application families, and at least one leave-one-environment-family-out transfer experiment.

**Mechanism evidence.** Per-cluster before/after recurrence, cluster extinction, new-failure emergence, failure-distribution shift, representative trajectory analysis, and tests that improvement is not simply memorization of generated variants.

**Reliability evidence.** Catastrophic-action rate, state corruption, unnecessary recovery, cost/latency, grader audit, human calibration, reward-hacking tests, contamination analysis, and complete generation/training provenance.

The local smoke suite validates instrumentation for these measurements. It does not satisfy the real-environment requirement and therefore cannot be used as a conference-result claim.

## v1.0 integration gate

The observation-aware model boundary and benchmark split manifest are implemented, so moving to a real interactive model should be a backend/configuration replacement rather than a rollout-methodology rewrite. This is an engineering readiness criterion only. Paper readiness still requires real model training/evaluation, held-out environment families, independent human annotations, and the full statistical protocol above.
