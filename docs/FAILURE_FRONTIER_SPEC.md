# Failure Frontier Specification

## Why stable mechanism identity matters

Independent clustering runs do not preserve cluster IDs. A longitudinal reliability study cannot infer that `cluster 3` at model v1 is the same mechanism as `cluster 3` at model v2. SORELIA therefore separates **within-round discovery** from **across-round identity**.

## Cluster signature

Each discovered cluster stores a centroid over structured failure features together with dominant task family/type, severity, recoverability, difficulty, temporal position and cluster entropy diagnostics.

## Matching

Adjacent rounds compute pairwise signature similarity. Primary identities are assigned with deterministic greedy one-to-one matching above a match threshold. A matched cluster inherits the prior stable mechanism ID. Unmatched prior clusters become extinct; unmatched current clusters become emergent.

Secondary high-similarity edges are retained to detect topology changes:

- **split** — one prior mechanism maps strongly to multiple current clusters
- **merge** — multiple prior mechanisms map strongly to one current cluster

These events matter because a training update can fragment a broad failure into narrower residual failures, or collapse several surface failures into one underlying mechanism.

## Risk mass

For cluster `c`:

`risk(c) = prevalence(c) × (0.5 + severity(c)) × (1.5 - recoverability(c))`

The exact formula is an explicit modeling choice and must be ablated in paper-scale work; it is not presented as a universal definition of risk.

## Transition statistics

Across an update SORELIA reports:

- total risk before / after
- net risk change
- risk removed
- risk introduced
- risk displacement ratio = introduced risk / removed risk
- extinction / contraction / persistence / expansion / emergence counts
- split / merge topology events

A displacement ratio above 1 indicates that more risk was introduced or expanded than removed/contracted under this operational definition, even if aggregate task success improved.

## Falsification test

The moving-frontier thesis is useful only if these longitudinal measures reveal meaningful differences that aggregate success or a static failure histogram misses. If they do not predict, explain or improve held-out reliability under equal budgets, the central hypothesis is not supported.


## Identity assignment
Primary one-to-one mechanism identity uses the Hungarian/linear-sum assignment on the full pairwise similarity matrix, followed by a preregistered similarity gate. This avoids greedy local matches that can lower global identity consistency. Split/merge topology events are detected separately using the event threshold.
