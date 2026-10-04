# SORELIA Experiments

**Author:** Aura Yavary  
**Evidence boundary:** retained engineering/methodology evidence; not frontier-model SOTA evidence.

This is the canonical experiment workspace entry point. It exists so opening `experiments/` gives an immediate view of what was executed, what failed, and what remains pending.

## Executed experiment families

1. **EXP-001 — Local closed-loop smoke**  
   End-to-end collect → cluster → allocate → verify → train → re-evaluate execution.
2. **EXP-002 — Chromium browser fixture**  
   Real DOM/action/recovery path on 12 isolated Chromium tasks.
3. **EXP-003 — Moving failure-frontier smoke**  
   Demonstrated that unchanged task success can coexist with adverse risk displacement.
4. **EXP-004 — Fixed-budget curriculum comparison**  
   Compared SORELIA with static priority, frequency, random, difficulty, and human-balanced curricula under equal verified-data budgets.
5. **EXP-005 — Repeated-trial / multiseed inference**  
   Added repeated stochastic trials, bootstrap intervals, and paired inference; no stable superiority claim emerged.
6. **EXP-006 — Shifted stress split**  
   Tested whether method ordering survived harder/longer perturbations; ordering changed.
7. **EXP-007 — Exploration ablation**  
   Tested exploration reserve; removing exploration sometimes improved IID smoke performance.
8. **EXP-008 — Semantic negative controls**  
   Shuffled labels and random clusters remained competitive in toy smoke, weakening causal semantic claims.
9. **EXP-009 — Matching ambiguity audit**  
   Quantified uncertain cross-round mechanism identity and motivated human-calibration gates.

Full hypothesis/setup/result/interpretation/next-decision entries are in `executed/` and summarized in `EXPERIMENT_MATRIX.md`.

## Retained results

- `results/browser_smoke.json`
- `results/v070_release_multiseed.json`
- `results/v100_compare.json`
- `results/v100_ablations.json`
- `results/V170_RELEASE_REPORT.json`

## Retained configs

See `configs/` for actual smoke/release configurations preserved with the release.

## Raw evidence

The deepest trajectories, frontiers, allocations, generated tasks, correction datasets, annotation packets, plots, and qualitative cases remain under `../artifacts/`. See `raw/README.md` for exact paths.

## Paper-scale work still pending

See `paper_scale/PENDING_EXPERIMENTS.md`. Those experiments are deliberately **not** claimed as completed.
