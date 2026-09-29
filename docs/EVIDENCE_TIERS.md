# Evidence tiers

SORELIA separates engineering validity from scientific claims.

1. **Tier 0 — unit/integration tests.** Schemas, clustering, generation, provenance, statistics, schedulers, and pipeline contracts.
2. **Tier 1 — deterministic state-machine sandbox.** Fast end-to-end closed-loop experiments and multi-seed smoke tests.
3. **Tier 2 — real browser fixture.** Chromium + Playwright executes DOM actions in an isolated local page; grading reads browser state. This validates the browser integration path without network instability or website-policy confounds.
4. **Tier 3 — controlled browser benchmark.** Required for paper claims: hundreds of tasks across independently authored sites/fixtures, held-out site families, perturbations, multiple model seeds, calibrated graders, and fixed-budget baselines.
5. **Tier 4 — frontier/trainable multimodal agent study.** Required before claiming results about modern computer-use agents.

The repository currently contains executed evidence through Tier 2. Tier 3/4 are protocols, not claimed results.
