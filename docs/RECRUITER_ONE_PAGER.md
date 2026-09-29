# SORELIA - One-page reviewer brief

**Aura Yavary**

## Thesis

Post-training can make an agent's aggregate score better while moving reliability risk somewhere else. SORELIA tracks the *moving failure frontier* across policy versions - extinction, contraction, persistence, expansion, emergence, split, and merge - and uses those dynamics to allocate the next fixed verified-data budget.

## Why this is not a generic "learn from failures" project

The repository explicitly treats failure-conditioned self-improvement as prior art. The narrower research question is longitudinal: **did the update remove risk, or displace it?** The benchmark therefore compares adaptive moving-frontier allocation against static failure-priority and failure-frequency curricula under equal verified-data budgets.

## What to inspect in five minutes

1. `docs/NOVELTY_AUDIT.md`
2. `src/sorelia/analysis/frontier.py`
3. `src/sorelia/curriculum/scheduler.py`
4. `src/sorelia/adapters/provider_agents.py`
5. `docs/TRUTH_AUDIT.md`
6. `paper/main.pdf`

## Engineering evidence

- local closed loop and real Chromium/Playwright fixture execute
- cross-version mechanism identity uses globally optimal gated matching
- exact train/eval leakage is release-blocking
- shuffled-label and random-cluster negative controls execute
- repeated trials and paired statistical tests are implemented
- benchmark/source/config hashes are recorded
- optional OpenAI Responses and Anthropic Messages adapters are offline-tested with injected clients
- token/cost accounting is measured-or-unknown; the harness does not invent usage
- null/adverse toy results are retained

## Truth boundary

No released result establishes frontier-model superiority, production reliability improvement, or completed human calibration. Provider adapters are integration code, not evidence that proprietary models were executed. The decisive next study is a real-agent, held-out-environment, multi-seed post-training experiment under the same budget and contamination controls.
