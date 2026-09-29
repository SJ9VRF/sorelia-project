# Reproducibility checklist

- fixed YAML configuration
- explicit random seeds
- deterministic synthetic task constructors
- versioned agent identifiers
- raw trajectory JSONL retained
- generated-task lineage retained
- equal training budgets across curriculum baselines
- held-out eval set separate from curriculum generation
- executable verifier for every local task
- tests runnable with `pytest -q`

For paper experiments additionally pin model checkpoints, browser/container images, package lock files, hardware, decoding parameters, number of trials, API/model versions and exact prompts/tool schemas.
