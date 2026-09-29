# SORELIA Dataset Card

## Purpose

The dataset format stores interactive-agent trajectories, structured failures, generated counterfactual tasks, verification outcomes, and curriculum provenance.

## Intended use

Research on agent evaluation, failure analysis, recovery-aware post-training and adaptive curriculum construction.

## Not intended for

Deployment decisions from the included local smoke-test data; claims about real-world browser or desktop reliability; training agents to act on live high-risk accounts.

## Fields

Trajectory: task/model/seed, observations, actions, expected and observed state, final state, success, failure and recovery events, grader outputs, tokens, latency, cost.

Failure: step, type, root cause, severity, recoverability, state transition mismatch, downstream effects, confidence.

Generated task: task family, target failure mode, difficulty, horizon, perturbations, source cluster and seed.

## Quality controls

Synthetic tasks must pass schema validation, deterministic reference-policy solvability, success-predicate validation and deduplication before use. Production data additionally needs contamination checks, model-grader calibration where used, and human review.

## Limitations

The local bundled dataset is generated from a simplified state-machine environment and should be treated only as a test fixture.
