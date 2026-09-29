# SORELIA Technical Report

**Aura Yavary**  
**SORELIA — Tracking and Training the Moving Failure Frontier of Interactive Agents**

## System objective

SORELIA studies whether a post-training update actually removes reliability risk or merely moves it. The system treats a model version not as a scalar success rate but as a distribution over failure mechanisms whose mass can disappear, persist, expand, contract, split, merge, or emerge after training.

## Runtime path

1. Execute repeated interactive rollouts against a deterministic/resettable environment.
2. Grade final and intermediate state using state-based verifiers.
3. Extract structured failure events with severity, recoverability, expected state, observed state, and correction candidates.
4. Discover failure mechanisms and preserve identity across policy versions using gated globally optimal bipartite matching.
5. Measure risk removed, risk introduced, frontier net change, topology events, and risk displacement.
6. Allocate an equal verified-data budget toward persistent, expanding, and emergent mechanisms while retaining exploration.
7. Generate counterfactual tasks and reject invalid, duplicate, leaking, or unverifiable variants.
8. Build correction/preference/training datasets and pass them to the configured post-training backend.
9. Re-evaluate IID and shifted stress splits and repeat.

## Agent boundary

The core is provider-independent. An `AgentDecision` may return an action plus measured token usage, model latency, optional explicit monetary cost, and provider metadata. Unknown usage is represented as unknown rather than silently converted to zero. Optional OpenAI Responses and Anthropic Messages adapters are shipped but proprietary frontier-model experiments are not claimed in the release.

## Failure identity

Cluster labels are not assumed stable across rounds. SORELIA matches mechanism signatures across adjacent versions, exposes assignment similarity and margin, marks ambiguous matches, and records split/merge topology. Blank annotation packets and a Cohen's-kappa scorer support independent human calibration without fabricating human judgments.

## Evaluation controls

- fixed verified-data budget across curriculum arms
- random, difficulty, frequency, human-balanced, and static failure-priority baselines
- shuffled-label and random-cluster negative controls
- repeated trials per task and multiple seeds
- paired bootstrap confidence intervals and paired permutation tests
- exact and near-duplicate train/eval contamination gates
- IID and deterministic shifted/stress evaluation
- run manifests, source/config hashes, benchmark manifests, evidence indexes, and claim-to-evidence auditing

## Safety

The environment contract distinguishes reversible, moderate, and high-risk actions. High-risk actions are intended for sandbox/mock execution unless an external product explicitly supplies a confirmation boundary. Catastrophic actions are tracked separately from ordinary task failure. Provider/parsing/infrastructure failures abort the experiment rather than being relabeled as model failures.

## Evidence boundary

The included local and Chromium runs are engineering evidence that the machinery executes. They do not establish state-of-the-art performance, production safety, human-validated mechanism identity, or superiority over frontier computer-use agents. Those claims require real-agent post-training, independently authored tasks, held-out environment families, adequate seeds/trials, strong published baselines, and independent human annotations.
