# SORELIA — Research Brief

**Aura Yavary**

## Thesis

Interactive-agent training changes the error distribution. Reliability therefore should be studied as a moving frontier, not a static list of failures. SORELIA tracks stable failure mechanisms across policy updates and reallocates a fixed verified-data budget according to what persists, expands, contracts, disappears or newly emerges.

## Why the question is nontrivial

A model can improve aggregate task success while creating a new class of high-severity errors. Static success metrics, static taxonomies and one-shot failure mining can miss this risk displacement.

## Method

1. collect held-out trajectories and state-based grader outcomes;
2. encode and cluster failure events by mechanism;
3. match cluster signatures across policy versions using stable IDs;
4. measure extinction, persistence, expansion, emergence, split/merge events and risk displacement;
5. allocate an equal verified-data budget toward the moving frontier;
6. generate counterfactual tasks with executable verifiers and lineage;
7. post-train, re-evaluate and repeat.

## Flagship experiment

Compare random, difficulty-only, human-balanced, failure-frequency, static failure-priority and SORELIA curricula with identical base model, optimizer, iterations and verified-data budget. Evaluate on held-out task instances, perturbations, failure mechanisms and environment families over multiple seeds.

## Success condition

SORELIA is interesting only if the dynamic frontier signal produces a reproducible held-out benefit over strong static curricula or reveals reliability regressions that aggregate success systematically misses.

## Current evidence boundary

The repository contains executable local and Chromium smoke paths, multi-seed statistics and longitudinal frontier instrumentation. It intentionally does not claim frontier-model or SOTA results before the paper-scale experiment is run.
