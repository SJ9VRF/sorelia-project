# SORELIA v1.0.0 - Research Harness Release

**Author: Aura Yavary**

v1.0.0 marks the point where SORELIA's public research harness has a stable, observation-aware interactive-agent boundary rather than a toy-only action API.

## New in v1.0

- observation-aware `DecisionContext`
- provider-agnostic `CallableInteractiveAgent`
- agent-supplied model identity in trajectories
- deterministic replay adapter for audited traces
- benchmark split manifest with task fingerprints and SHA-256 split identity
- `sorelia doctor` runtime readiness report
- browser smoke revalidated after the model-boundary change
- 29 passing source-tree tests
- 20 claim/evidence entries passing release audit

## What v1.0 means - and does not mean

It means the research methodology and evidence path can accept a real interactive model without changing the rollout contract.

It does **not** mean that frontier VLM/LLM post-training has been run, that SORELIA beats published systems, or that the paper's central hypothesis has been established. Those remain paper-scale empirical gates.
