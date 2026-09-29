# Implementation gates

## G0 — Contracts and schemas
Exit criteria: versioned task/trajectory/failure schema, environment and agent contracts, config-driven runner, tests.

## G1 — Real rollout collection
Add isolated browser fixtures, screenshot + accessibility-tree observations, deterministic reset, trace viewer and state-based graders.

## G2 — Failure representation
Add multimodal/structured embeddings, root-cause annotation, HDBSCAN, cluster stability analysis and human coherence calibration.

## G3 — Curriculum scheduler
Add uncertainty, learnability and expected-generalization-gain estimators; compare heuristic scheduling with a contextual-bandit allocator.

## G4 — Counterfactual generation
Implement typed mutation grammars by UI primitive and task family. Require executable verifiers and provenance.

## G5 — Post-training
Start with LoRA SFT; then preference optimization on good/bad actions and recovered/failed trajectories. Add online RL only after curriculum effects are identifiable without RL instability.

## G6 — Closed loop
Run >=3 full generations; preserve a replay/exploration mixture; measure failure-distribution shift and novel failure emergence.

## G7 — Paper experiments
Multiple seeds, fixed-budget baselines, held-out families, negative controls, ablations, confidence intervals, human calibration and cost analysis.

## G8 — Release
Code, benchmark adapters, dataset card, model card, paper, technical report, interactive explorer, demo video and exact reproduction commands.
