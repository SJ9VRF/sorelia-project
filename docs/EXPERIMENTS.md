# Paper-scale experiment plan

## Main comparison

Use the same base model, **verified-data budget**, task suite, number of trials and optimizer for:

1. Random synthetic curriculum
2. Difficulty-only curriculum
3. Human-designed balanced curriculum
4. Failure-frequency curriculum
5. Static failure-priority curriculum
6. SORELIA adaptive curriculum

Run at least 3 independent training seeds and >=5 eval trials per task when the policy/environment is stochastic.

## Evaluation splits

- in-distribution held-out instances
- unseen surface/UI perturbations
- unseen failure variants
- held-out task families
- leave-one-environment-family-out transfer

## Core claims

A. Fixed-data sample efficiency: higher held-out success for the same number of training trajectories.

B. Targeted correction: selected failure modes recur less often after training than matched controls.

C. Generalization: gains persist on variants not generated from the exact source task.

D. Adaptation: a multi-iteration adaptive scheduler outperforms a static failure-conditioned curriculum.

## Required ablations

- no clustering
- shuffled failure labels
- random cluster assignment
- frequency-only prioritization
- no severity weighting
- no uncertainty/learning-value weighting
- no verifier
- no recovered trajectories
- success-only data
- correction-only data
- no counterfactual mutation
- static curriculum
- single iteration
- 100% exploitation vs exploration mixture

## Negative controls

- allocate equal training data to unrelated failure families
- permute failure-to-curriculum mapping
- use matched-volume random variants

If these controls perform as well as SORELIA, the mechanism claim is not supported.

## Statistics

- task-level bootstrap 95% confidence intervals
- report mean and median where cost/latency are skewed
- paired task comparisons where possible
- per-family tables, not only aggregate metrics
- effect sizes as well as p-values
- disclose all seeds and rejected task counts

## Human calibration

Manually review 5–10% of trajectories and generated tasks. Double-annotate a subset for failure root cause and cluster coherence; report inter-rater agreement.

## Data-collapse study

Run >=4 curriculum iterations and measure:

- success
- task diversity
- failure entropy
- cluster extinction
- newly emerging failures
- held-out generalization

Compare 100% exploitation with an 80/20 failure-driven/exploration mixture.


## Benchmark-contract invariants

The implementation enforces these invariants rather than leaving them as prose:

- each method receives exactly `generation.budget` verified training tasks per iteration;
- only SORELIA receives longitudinal frontier-transition state; static baselines never see future/frontier labels;
- SORELIA comparison rounds after the first must expose a non-empty frontier transition report;
- run manifests hash the config and source tree used to produce comparison artifacts.

`tests/test_compare_contract.py` is the executable guardrail for these invariants.


## Executable core ablations

`python -m sorelia.cli ablate ...` currently executes: full SORELIA, static-priority/no-frontier adaptation, no exploration, single iteration, shuffled failure labels, and random cluster assignment. Model/data-path ablations (no verifier, no recovery data, success-only, correction-only) remain mandatory for the real trainable-agent study and are not claimed as executed locally.
