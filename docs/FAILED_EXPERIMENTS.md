# What did not work — failed hypotheses and invalidated assumptions

These are not retrofitted drama. Each item is grounded in retained outputs, implementation corrections, or negative-control results.

## F1 — “Frontier-aware curriculum should beat simpler curricula in the toy harness”
**What happened:** It did not. In retained fixed-budget runs, human-balanced, static-priority, frequency, and random-cluster controls sometimes matched or beat full SORELIA.

**Evidence:** `docs/RESULTS_V080_ROBUSTNESS.md`, `docs/RESULTS_V090_INTEGRITY.md`.

**Why we think it happened:** The synthetic environment is small and structured enough that simple heuristics can exploit task regularities; it is not a convincing causal test of semantic failure tracking.

**Change:** Preserve the result, strengthen controls, and move the main hypothesis to real interactive agents. The toy harness does not support a SORELIA superiority claim.

## F2 — “Exploration reserve should monotonically help”
**What happened:** Removing exploration sometimes improved IID success in the toy ablation.

**Evidence:** `docs/RESULTS_V080_ROBUSTNESS.md`, v0.9 integrity ablations.

**Change:** Treat exploration as a tunable intervention and require an ablation instead of assuming benefit.

## F3 — Coarse `(family, failure_type)` identity was too weak
**What happened:** Distinct mechanisms could collapse into the same coarse label across rounds.

**Change:** Replaced with cluster signatures, globally optimal gated matching, stable IDs, ambiguity margins, and split/merge events.

## F4 — Greedy cross-round matching was methodologically brittle
**What happened:** Greedy assignment could consume a locally good match and force a globally worse identity map.

**Change:** Replaced with Hungarian/global bipartite assignment under a similarity gate; added regression tests.

## F5 — The v0.5 comparison mislabeled a legacy allocator as SORELIA
**What happened:** The comparison path used the old static allocator for the arm named `sorelia`.

**Why it matters:** Any advantage/disadvantage from that comparison could not be attributed to the moving-frontier method.

**Change:** Corrected the harness in v0.6, regenerated evidence, enforced equal verified-data budgets, and added a regression test.

## F6 — Synthetic token/cost accounting created false precision
**What happened:** Early rollouts assigned fixed token/cost values to local actions.

**Change:** Removed synthetic accounting. Unknown usage/cost is now `null` with explicit coverage fractions. Provider/infrastructure errors are also separated from scientific failures.
