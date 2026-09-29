# Statistical protocol

SORELIA treats agent outcomes as stochastic repeated measurements rather than one deterministic score per task.

## Unit of evaluation

The primary unit is a **task × trial** cell. Repeated trials receive distinct seeds and IDs. Main paper results must report at least 5 independent model/training seeds and at least 3 trials per held-out task unless compute constraints are explicitly disclosed.

## Primary comparison

For each seed, SORELIA and every baseline use the same benchmark construction, verified-data budget, iteration count, and training procedure. Final metrics are compared across matched seeds.

We report:

- mean and bootstrap 95% CI for each method;
- paired SORELIA-minus-baseline mean difference with paired bootstrap 95% CI;
- a two-sided paired randomization/permutation test;
- raw per-seed values, never only aggregate bars.

A paper claim of superiority requires the effect direction to be consistent with the metric, the paired confidence interval to exclude zero, and the randomization test to pass the preregistered alpha after multiple-comparison correction when more than one primary endpoint is tested.

## Primary endpoints

1. held-out task success rate;
2. persistent/expanding failure risk mass;
3. risk displacement ratio.

Secondary endpoints include failures/task, catastrophic-action rate, recovery rate, cost, latency, and steps.

## Multiple comparisons

The paper-scale protocol will declare primary endpoints before execution. Secondary analyses are exploratory. If several baselines are tested against SORELIA on the same primary endpoint, Holm correction should be applied to paired p-values.

## Failure-frontier identity uncertainty

Cross-round cluster identity is established with globally optimal bipartite assignment under a similarity threshold. Split/merge events use a separate event threshold. Threshold sensitivity is an ablation, not a tuning knob selected on test performance.

## Negative and null results

Null or adverse results remain in the artifact. A rise in aggregate success does not count as reliability improvement if newly introduced risk offsets removed risk. This is why risk removed, risk introduced, and displacement are reported separately.


## Stress/OOD reporting

Report IID and shifted/stress metrics separately. Do not collapse them into one headline score. The local stress split is a harness check, not a substitute for held-out real websites or environment families.

## Frontier matching calibration

For each primary cross-round mechanism match, report cosine/signature similarity and the margin over the best competing assignment touching either endpoint. Flag margins below 0.05 as ambiguous in the reference harness. Paper-scale work should calibrate this threshold against human-labeled mechanism identity.
