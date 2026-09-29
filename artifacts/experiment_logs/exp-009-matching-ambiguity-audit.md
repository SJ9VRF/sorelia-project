# EXP-009 — Matching ambiguity audit

**Evidence tier:** engineering smoke / methodology validation, not frontier-model performance evidence.

## Hypothesis
Are cross-round mechanism identities certain enough to be treated as ground truth?

## Setup
Optimal bipartite matching with similarity margins and ambiguity flags.

## Result
The v0.9 integrity run reported 25% ambiguous matches; a later local frontier example reported 50% ambiguity among matched mechanisms.

## Interpretation
Automatic mechanism identity is not validated ground truth.

## Next decision
Generate blank human calibration packets and block validated-identity claims until independent annotations exist.
