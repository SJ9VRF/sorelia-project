# EXP-007 — Exploration ablation

**Evidence tier:** engineering smoke / methodology validation, not frontier-model performance evidence.

## Hypothesis
Does reserving exploration budget reliably improve the adaptive curriculum?

## Setup
Full SORELIA vs no-exploration ablation under the same local harness.

## Result
In retained toy runs, removing exploration sometimes improved IID success; the effect was not monotonic.

## Interpretation
The intuitive "exploration always helps" hypothesis failed in the toy setting.

## Next decision
Treat exploration ratio as an empirical hyperparameter and report ablation, not a default virtue.
