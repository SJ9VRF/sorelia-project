# Release status — v1.7.0

## Executable and tested in this release

The following components are implemented and exercised locally:

- deterministic long-horizon state-machine environment
- real Chromium + Playwright isolated browser fixture backend
- reset / observe / action / verify / rollback browser loop
- stochastic trainable reference policy
- full trajectory, failure and recovery logging
- structured failure embeddings and within-iteration clustering
- **stable cluster-signature matching across policy versions**
- failure-frontier states: extinct, contracting, persistent, expanding, emergent
- split/merge topology-event detection
- risk removed, risk introduced, net risk change and risk-displacement ratio
- transition-aware curriculum allocation with exploration reserve
- equal-budget random, difficulty, human-balanced and failure-frequency baselines
- counterfactual mutation, duplicate filtering and executable verification
- generation provenance and stable mechanism IDs
- cumulative supervised training plus correction/preference data construction
- repeated SORELIA iterations and held-out evaluation
- multi-seed aggregation and bootstrap confidence intervals
- unit/integration/browser/provider-adapter tests, CLI and CI
- measured usage accounting with unknown-vs-zero semantics
- optional OpenAI Responses and Anthropic Messages adapters, offline-tested via injected fake clients

The v1.7.0 source-tree suite passes **57 tests** in the artifact environment.


## v1.1 provider and accounting hardening

- Removed synthetic per-action token and cost accounting.
- Added `AgentDecision` for measured provider usage and model latency.
- Aggregate cost/token metrics now report coverage and use `null` when unknown.
- Added optional OpenAI Responses and Anthropic Messages adapters without claiming proprietary-model execution.
- Provider parsing errors remain infrastructure/interface errors rather than scientific task failures.
- Rollout cleanup uses `finally` so browser/environment resources close even when a model backend raises.

## v1.0 architecture hardening

- Replaced the toy-only `act(task, step)` decision boundary with an observation-aware `DecisionContext` carrying current observation, expected state, bounded history, task metadata, and determinism intent.
- Added `CallableInteractiveAgent` as a provider-agnostic integration boundary for API-backed or local multimodal agents without coupling provider SDKs to SORELIA core.
- Removed the hard-coded rollout `model_id`; trajectories now record the adapter/model identity supplied by the agent.
- Added immutable benchmark split manifests with per-task fingerprints and split-level SHA-256 digests.
- Added `sorelia doctor` to report core runtime readiness separately from optional browser integration readiness.
- Added contract tests for the real-model adapter boundary, benchmark-manifest determinism, and runtime doctor.

## What these executions prove

They prove that the research machinery is executable and internally auditable: SORELIA can discover a failure frontier, match mechanisms across updates, observe topology changes, allocate data budget, train the next reference policy and re-evaluate the result. They do **not** prove that SORELIA improves a frontier model.

## Deliberately not claimed

The release does not claim completion of:

- frontier VLM/LLM SFT, preference optimization or RL
- uncontrolled external-site computer-use benchmarks
- hundreds of independently authored tasks
- human failure-label / grader calibration study (protocol and scorer implemented; real annotations pending)
- paper-scale ablation matrix
- held-out website/application-family generalization at scale
- GPU-scale distributed post-training
- statistically supported superiority over strong published systems

## Paper claim gate

A result can be promoted from engineering evidence to a paper claim only after: real interactive-agent model; held-out task and environment families; equal verified-data and optimization budgets; at least five seeds; confidence intervals; contamination checks; human calibration; required ablations and negative controls; complete lineage; and no post-hoc task/seed filtering.


## v0.7.0 release corrections

- Fixed a material benchmark-contract bug: the `compare` path previously labeled a static scheduler as SORELIA. It now carries cluster state across iterations and calls the moving-frontier allocator from round 2 onward.
- Enforces the same verified-data budget for every curriculum on every iteration.
- Adds run manifests with config/source hashes and platform metadata.
- Adds per-run evidence indexes and a claim-to-evidence release audit.
- Current source-tree suite: 15 tests pass.

This correction is intentionally documented rather than hidden: the benchmark harness is part of the scientific claim and must be auditable.


### v0.7 statistical/identity hardening
- Cross-round cluster identity uses globally optimal bipartite assignment under a similarity gate.
- Evaluation supports repeated task trials.
- Multiseed output includes paired bootstrap effect intervals and paired randomization tests against every baseline.


### v0.8 robustness hardening

- Added the missing static failure-priority baseline promised by the experimental protocol.
- Added executable shifted/stress evaluation and separate stress metrics.
- Added matching-confidence diagnostics for longitudinal identity.
- Added executable core ablations and retained mixed/adverse outcomes.
- Full real-agent OOD and human-calibrated matching studies remain paper-scale gates. v0.9 implements exact leakage gates, negative controls, and the blank annotation/scoring infrastructure, but does not claim completed human calibration.

## v1.6.0 public artifact additions

The release now includes standalone architecture/frontier figures, a portfolio project card, evidence-grounded trajectory-replay MP4, interview talk tracks, demo narration, résumé-safe wording, and a tested 14-section flagship project page. These additions do not change the scientific evidence tier.

## v1.6.0 public-repository hardening

The public snapshot now includes contribution/security/conduct policies, benchmark and system cards, an executed-vs-pending experiment registry, a research decision log, reviewer reproduction instructions, GitHub issue/PR templates, and a one-command reviewer demo. These additions improve auditability and maintenance quality; they do not upgrade engineering smoke evidence into paper-scale model results.

## v1.6.0 Evidence Layer
Added a public experiment journal, failed-experiment record, structured decision log, unexpected findings, curated raw artifacts, real-from-now-on Git history, and homepage research-process layer. No historical commits or unexecuted results were fabricated.
