# Paper-scale Experiments — Pending, Not Claimed

These experiments are required before SORELIA can support scientific superiority, SOTA, production-reliability, or human-validated mechanism-identity claims.

## Required main study

- real trainable interactive VLM/agent
- real post-training rather than the local policy update surrogate
- independently authored browser/desktop task suites
- held-out website/application/environment-family splits
- >=5 independent training seeds
- >=5 stochastic evaluation trials per task where applicable
- fixed verified-data budgets across methods
- strong published-agent / strong curriculum baselines
- task-level bootstrap confidence intervals and paired inference

## Required data-path ablations

- no verifier
- no recovered trajectories
- success-only training data
- correction-only training data
- no counterfactual mutation
- no clustering
- shuffled labels
- random cluster assignment
- frequency-only/static-priority allocation
- no exploration / exploration sweep

## Required human calibration

- independently annotated mechanism identity on a held-out subset
- inter-rater agreement
- precision/recall of automatic matching against adjudicated labels
- calibration of ambiguity threshold

## Falsification criteria

The central mechanism claim is weakened or rejected if:

1. static/frequency/random-cluster controls match SORELIA under equal verified-data budget;
2. frontier transitions are not stable under human calibration;
3. gains disappear on held-out environment families;
4. risk-displacement metrics do not predict meaningful downstream reliability differences;
5. improvements depend on train/eval leakage or generator-specific artifacts.
