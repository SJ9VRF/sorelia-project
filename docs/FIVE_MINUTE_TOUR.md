# SORELIA in five minutes

**Researcher: Aura Yavary**

## 1. Read the scientific question

Start with `README.md` and `docs/NOVELTY_AUDIT.md`.

SORELIA does not claim that learning from failures is new. The narrower question is whether the *movement* of failure mechanisms across policy updates can be used to allocate the next fixed training budget more effectively without displacing risk into new failure modes.

## 2. Inspect the scientific object

Read `src/sorelia/analysis/frontier.py` and `docs/FAILURE_FRONTIER_SPEC.md`.

Cluster IDs are not assumed stable. Discovered mechanism signatures are matched across updates, stable IDs are inherited, split/merge events are recorded, and ambiguous matches expose confidence margins for human calibration.

## 3. Inspect the intervention

Read `src/sorelia/curriculum/scheduler.py` and `src/sorelia/experiments.py`.

The comparison keeps verified-data budgets equal. Only SORELIA receives longitudinal frontier state; static-priority, frequency, difficulty, random, and manually balanced curricula remain distinct baselines.

## 4. Verify the real-agent boundary

Read `docs/MODEL_ADAPTER_CONTRACT.md`, `src/sorelia/schema.py`, `src/sorelia/adapters/model_agent.py`, and `src/sorelia/infra/rollout.py`.

The policy receives an observation-aware `DecisionContext`. Provider-specific SDKs stay outside the research core. The released local policy is deliberately small; no proprietary frontier-model experiment is implied.

## 5. Verify benchmark identity and integrity

Inspect `artifacts/v100_smoke/benchmark_manifest.json`, `docs/CONTAMINATION_PROTOCOL.md`, and `docs/EVIDENCE_MAP.md`.

Every flagship run freezes train/eval identity with fingerprints and split hashes before training. Exact leakage blocks the run; near-duplicate diagnostics are reported.

## 6. Reproduce the release gate

```bash
PYTHONPATH=src python -m sorelia.cli doctor
bash scripts/reproduce_release.sh
```

The release gate runs tests, source compilation, claim/evidence audit, an end-to-end loop, fixed-budget comparison, negative-control ablations, leakage checks, frontier invariants, benchmark-manifest checks, and matching-calibration packet generation.

## 7. Check the truth boundary

Read `docs/TRUTH_AUDIT.md`, `docs/RELEASE_STATUS.md`, and `docs/RESULTS_V090_INTEGRITY.md`.

The local evidence contains mixed and adverse results by design. It demonstrates that the harness can falsify the project narrative; it does not establish frontier-agent superiority.

## 8. Decide whether the thesis survives the real experiment

The flagship paper claim should be accepted only if equal-budget, real-agent experiments show lower persistent/expanding risk and no compensating emergent risk on held-out environments with repeated seeds, human calibration, and required ablations. Otherwise the central hypothesis should be rejected.
