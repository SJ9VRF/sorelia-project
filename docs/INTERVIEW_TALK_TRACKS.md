# Interview talk tracks — SORELIA

## 30 seconds
SORELIA studies a failure mode in agent post-training that scalar success rates hide. After an update, one failure mechanism can disappear while another emerges or expands. I built a system that discovers failure mechanisms, matches them across policy versions, measures risk removed versus introduced, and reallocates a fixed verified training-data budget toward the moving frontier. The important part is that the evaluation can falsify the idea: the released smoke tests preserve runs where SORELIA loses to static or random baselines.

## 60 seconds
Most failure-driven agent loops ask which failed trajectories should become training data. I wanted to ask a stricter question: after training, where did the failures go? SORELIA tracks stable failure-mechanism identity across policy versions, including ambiguous matches and split/merge events. It classifies mechanisms as extinct, contracting, persistent, expanding, or emergent; measures risk displacement; and uses those transitions to allocate the next fixed verified-data budget. I implemented the rollout/eval stack, browser fixture, clustering and longitudinal matching, transition-aware scheduler, synthetic-task verification, leakage gates, negative controls, repeated-trial statistics, provider boundaries, and claim-to-evidence audit. Current public numbers are engineering smoke evidence, not frontier-model claims.

## 5 minutes
1. **Problem:** final success hides causal failure structure and can stay flat while risk migrates.
2. **Insight:** treat the failure distribution as a longitudinal frontier, not a static dataset.
3. **Method:** evaluate → discover mechanisms → optimally match across rounds → measure transitions/risk → allocate equal training budget → verify tasks → train → re-evaluate.
4. **Hard technical choices:** stable mechanism identity, ambiguity margins, split/merge topology, fixed-budget baselines, unknown-cost semantics, contamination blocking.
5. **Evidence discipline:** local/Chromium smoke tests prove the harness works; negative/null outcomes are kept; no SOTA claim.
6. **What I would run next:** real trainable computer-use model, held-out application families, 5+ training seeds, human mechanism labels, full data-path ablations.

## Likely deep-dive questions
**Why not just use failure frequency?** Because frequency is a snapshot. SORELIA tests whether the *transition* after an update contains additional allocation signal. Static failure-priority is therefore a required baseline.

**How do you know a failure is the same mechanism across versions?** Within-round clusters get structured signatures; adjacent rounds are matched with globally optimal gated assignment. Similarity, assignment margin, ambiguity, and split/merge secondary edges are recorded. Human calibration is designed but not fabricated.

**What would falsify the thesis?** If transition-aware allocation does not beat strong static allocation under equal data/compute on real agents, or if gains disappear on held-out environments, the central claim should be narrowed or rejected.

**What is the strongest current limitation?** The released evidence proves the research machinery, not the empirical superiority claim. Real post-training and independent human calibration remain pending.
