# Contamination and leakage protocol

SORELIA treats train/eval leakage as a release-blocking methodological error.

## Executable local gate

Before each training update, cumulative verified training tasks are compared against held-out evaluation tasks using:

1. exact task-ID overlap;
2. exact semantic fingerprints over family, failure mode, difficulty, horizon, perturbations, and normalized instruction;
3. a structural near-duplicate diagnostic within the same family/failure mechanism.

Exact ID or semantic overlap raises an exception. Near-duplicate pairs are reported separately because the threshold is a diagnostic modeling choice, not a universal definition of contamination.

## Paper-scale extension

For real browser/desktop benchmarks, the contamination audit must additionally cover:

- source site/domain and template ancestry;
- task author identity and shared fixture lineage;
- copied or paraphrased instructions;
- generated-task ancestry from held-out traces;
- model pretraining contamination when benchmark provenance makes this assessable;
- screenshots/DOM templates that differ cosmetically but encode the same held-out task instance.

A held-out environment/site family must never be used to generate training tasks for the experiment that claims transfer to that family.
