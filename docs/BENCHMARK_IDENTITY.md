# Benchmark Identity and Split Manifest

Every flagship end-to-end run writes `benchmark_manifest.json` before training begins.

For each split (`train`, `eval`, optional `stress`) it records:

- task ID
- task family
- intended failure mode
- seed
- deterministic task fingerprint
- split-level SHA-256 digest

This makes the exact benchmark identity reviewable independently of the runtime log and complements the contamination gate. If a task definition, seed, or split assignment changes, the corresponding digest changes.

A benchmark manifest does not by itself prove external benchmark validity. It proves only that the released experiment's split identity is explicit and hashable.
