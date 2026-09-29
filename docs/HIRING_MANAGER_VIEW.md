# Hiring-manager view: SORELIA

**Aura Yavary**

# What a strong hiring manager should see

**Project:** SORELIA — Tracking and Training the Moving Failure Frontier of Interactive Agents  
**Researcher:** Aura Yavary

The high-signal story is not "I built another agent loop." It is:

> I found that the obvious failure-driven self-improvement idea was already crowded, audited the literature, narrowed the question, and changed both the implementation and the experimental contract. SORELIA now studies whether training actually removes failure risk or merely moves it somewhere else.

That signals research judgment because the project explicitly contains its own falsification machinery: equal-budget baselines, transition tracking, new-failure emergence, held-out environments, negative controls, multi-seed uncertainty, and a truth audit separating executable infrastructure from unrun frontier-scale claims.

## What would make it genuinely impressive

A final public release should show at least one nontrivial real-agent finding that would have been invisible under ordinary task-success evaluation—for example, two methods with similar final success but materially different persistent/expanding/emergent risk. The result should survive multiple seeds and held-out environment families.

## What would make it look synthetic or weak

- dozens of generic modules without one sharp empirical question
- broad "self-improving agent" claims that ignore WebRL/UI-Genie and 2026 failure-learning work
- decorative dashboards before real experiments
- SOTA language attached to toy environments
- exact percentages that are not reproducible from public scripts
- a homepage that lists buzzwords instead of one surprising result

SORELIA should remain small enough that every visible artifact supports the moving-failure-frontier thesis.

## What changed in v0.6.0 that matters scientifically

The comparison harness was audited and a real methodological bug was found: the arm labeled SORELIA was still using the legacy static allocator. That is now corrected. The benchmark path carries longitudinal cluster state only for SORELIA, invokes transition-aware allocation from the second round onward, and enforces identical verified-data budgets across all curricula. A regression test locks this contract.

That correction is intentionally visible in the changelog and release status. The point of the project is not to present an immaculate-looking story; it is to demonstrate research judgment strong enough to find, disclose, and fix a flaw that could otherwise invalidate the central comparison.


## What changed in v0.7.0 that matters scientifically
The mechanism tracker now uses globally optimal gated bipartite assignment rather than greedy identity matching. Evaluation supports repeated task trials, and multiseed comparisons report paired bootstrap effect intervals plus paired randomization tests. The retained release smoke is adverse/null for SORELIA on task success, which is evidence that the harness can falsify the desired hypothesis rather than manufacture a win.

## What changed in v0.8.0 that matters scientifically
The benchmark gained a distinct static-priority baseline, an executable shifted/stress split, match-margin ambiguity diagnostics, and executable core ablations. This made it possible to separate longitudinal frontier information from simpler static failure prioritization and to inspect robustness rather than only IID task success.

## What changed in v0.9.0 that matters scientifically
The integrity layer is now part of the method, not a documentation promise. Cumulative training data is gated against held-out evaluation by task ID and semantic fingerprint; near-duplicate diagnostics are reported separately. Shuffled-failure-label and random-cluster-assignment controls are executable. Every end-to-end run emits a blank cross-round mechanism annotation packet, and the repository can score inter-annotator agreement and matcher-vs-human calibration once independent humans supply labels. The local toy ablation does not favor SORELIA consistently, and that adverse evidence is retained rather than tuned away.

## v1.0 research-engineering boundary

The most important v1.0 change is architectural rather than cosmetic. Rollouts no longer assume a toy policy that sees only `(task, step)`. Every policy now receives an observation-aware `DecisionContext`, while provider-specific SDK/authentication code remains outside the research core through `CallableInteractiveAgent`. Trajectories record the adapter-supplied model identity, and end-to-end runs freeze their train/eval benchmark identity in a fingerprinted split manifest before training.

That makes the next experiment a backend replacement rather than a methodology rewrite: plug in an isolated real browser/desktop environment and a trainable/API-backed interactive model, then run the same contamination, budget, frontier, negative-control, calibration, and evidence paths.

The released evidence still does **not** demonstrate frontier-model superiority. That gap is explicit and is the next scientific gate, not something hidden behind the local smoke tests.
