# EXP-004 — Fixed-budget curriculum comparison

**Evidence tier:** engineering smoke / methodology validation, not frontier-model performance evidence.

## Hypothesis
Does frontier-aware allocation dominate simpler curricula under equal verified-data budgets?

## Setup
Same base policy, optimization path, eval set and verified training-data budget; compare SORELIA, static priority, frequency, random, difficulty and human-balanced.

## Result
In the retained v0.8 smoke, SORELIA did not win: human-balanced had best IID success (99.07%); frequency had best stress success (96.30%).

## Interpretation
The toy harness does not support a SORELIA superiority claim. Equal-budget controls are necessary because plausible simpler baselines remain strong.

## Next decision
Retain null/adverse results and move superiority claims behind real-agent experiments.
