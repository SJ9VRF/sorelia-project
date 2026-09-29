# v0.8.0 robustness, calibration, and ablation smoke

These are engineering smoke tests in the synthetic local harness. They are not claims about frontier computer-use agents.

## What changed

- Added a real static failure-priority baseline to the fixed-budget comparison.
- Added a deterministic shifted/stress split with harder tasks, longer horizons, and stronger perturbations.
- Added cross-round matching calibration (mean similarity, assignment margin, ambiguous-match rate).
- Added executable core ablations: full SORELIA, static priority, no exploration, and single iteration.

## Single-seed fixed-budget smoke (final iteration)

| Method | IID success | Stress success | IID failures/task | Stress failures/task | Catastrophic rate |
|---|---:|---:|---:|---:|---:|
| SORELIA | 0.9769 | 0.9444 | 0.5324 | 0.5556 | 0.0185 |
| Static priority | 0.9815 | 0.9444 | 0.5093 | 0.5926 | 0.0185 |
| Frequency | 0.9630 | 0.9630 | 0.6250 | 0.3333 | 0.0278 |
| Random | 0.9630 | 0.9444 | 0.5231 | 0.4444 | 0.0185 |
| Difficulty | 0.9769 | 0.9444 | 0.5185 | 0.3889 | 0.0093 |
| Human-balanced | 0.9907 | 0.9444 | 0.3981 | 0.3704 | 0.0093 |

No superiority claim is supported by this smoke run.

## Core ablation smoke

The executable ablation harness also produced mixed results. In this small run, removing exploration improved IID success while full SORELIA had higher stress success than the no-exploration variant. This is exactly why exploration policy must be tested rather than assumed beneficial. See `artifacts/v080_ablations.json`.

## Two-seed repeated-trial robustness smoke

A small two-seed run was executed to validate stress-metric aggregation and paired inference plumbing. SORELIA mean final IID success was 0.875 and stress success was 0.9583; several baselines were higher on one or both metrics. This run is too small for scientific conclusions and is retained specifically to demonstrate that the harness preserves adverse/null outcomes. See `artifacts/v080_multiseed.json`.

## Interpretation boundary

The stress split changes difficulty/horizon/perturbation intensity but does not constitute real website-family OOD generalization. Paper-scale claims still require real browser agents, independently authored tasks, held-out sites/environments, human calibration, and adequate seeds.
