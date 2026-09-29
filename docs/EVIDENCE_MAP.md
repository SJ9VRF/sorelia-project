# Evidence map - v1.0.0

This is the shortest path from a public claim to executable evidence.

| Question | Evidence |
|---|---|
| Does the core loop actually execute? | `artifacts/v100_smoke/metrics.json`, `artifacts/v100_smoke/frontier_i2.json` |
| What exact code/config produced the run? | `artifacts/v100_smoke/run_manifest.json` |
| What exact benchmark split was used? | `artifacts/v100_smoke/benchmark_manifest.json` |
| Are output files integrity-indexed? | `artifacts/v100_smoke/evidence_index.json` |
| Does the benchmark compare the moving-frontier method under fixed verified-data budgets? | `src/sorelia/experiments.py`, `tests/test_compare_contract.py`, `artifacts/v100_compare.json` |
| Do negative controls and core ablations execute? | `src/sorelia/experiments_ablation.py`, `tests/test_negative_controls.py`, `artifacts/v100_ablations.json` |
| Does real browser execution exist? | `src/sorelia/adapters/playwright_env.py`, `tests/test_playwright_env.py`, `artifacts/browser_smoke.json` |
| Can a real model backend receive observations/history without rewriting the rollout core? | `src/sorelia/schema.py`, `src/sorelia/adapters/model_agent.py`, `tests/test_model_adapter_contract.py` |
| Is matching uncertainty visible to human calibration? | `artifacts/v100_smoke/matching_annotation_packet_i2.jsonl`, `docs/HUMAN_CALIBRATION_PROTOCOL.md` |
| Which claims are explicitly unsupported? | `docs/CLAIM_EVIDENCE_REGISTRY.json`, `docs/TRUTH_AUDIT.md` |

Run `PYTHONPATH=src python -m sorelia.cli audit --root .` before publishing.
