# EXP-008 — Semantic negative controls

**Evidence tier:** engineering smoke / methodology validation, not frontier-model performance evidence.

## Hypothesis
Does the method depend on meaningful failure labels/clusters?

## Setup
Shuffled failure labels and random cluster assignment, alongside full SORELIA and static priority.

## Result
In v0.9 smoke, random clusters and static priority outperformed full SORELIA on IID success; shuffled labels also remained competitive.

## Interpretation
Toy task structure may provide enough non-semantic signal that the current environment cannot establish causal value of semantic mechanism tracking.

## Next decision
Require stronger real-agent tasks and retain negative controls as a falsification gate.
