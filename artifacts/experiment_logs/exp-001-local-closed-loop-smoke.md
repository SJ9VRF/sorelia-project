# EXP-001 — Local closed-loop smoke

**Evidence tier:** engineering smoke / methodology validation, not frontier-model performance evidence.

## Hypothesis
Can the complete collect→cluster→allocate→verify→train→reevaluate loop execute reproducibly?

## Setup
Local synthetic environment; deterministic state-based graders; fixed seed.

## Result
The end-to-end loop executed and emitted trajectories, clusters, allocations, verified tasks, corrections, metrics and manifests.

## Interpretation
The system was executable, but success alone was insufficient to characterize what changed in the failure distribution.

## Next decision
Add longitudinal failure-frontier instrumentation rather than only aggregate success.
