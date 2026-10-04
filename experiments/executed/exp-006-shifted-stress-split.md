# EXP-006 — Shifted stress split

**Evidence tier:** engineering smoke / methodology validation, not frontier-model performance evidence.

## Hypothesis
Do conclusions survive a deterministic harder/longer perturbation split?

## Setup
IID and shifted/stress split with increased difficulty, horizon and perturbation intensity.

## Result
Methods changed ordering between IID and stress metrics; frequency led stress success in the retained v0.8 single-seed smoke while human-balanced led IID.

## Interpretation
A single IID aggregate can hide robustness differences. The stress split is useful plumbing but not real website-family OOD.

## Next decision
Keep separate stress metrics and require held-out real environments before ecological-generalization claims.
