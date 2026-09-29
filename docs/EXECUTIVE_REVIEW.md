# SORELIA - Executive Research Review

**Aura Yavary**  
**Project:** Tracking and Training the Moving Failure Frontier of Interactive Agents

## The one-sentence thesis

After an agent is post-trained, reliability risk does not simply go down - it can disappear, persist, split, merge, expand, or re-emerge elsewhere. SORELIA treats that moving failure frontier as the signal for allocating the next fixed training budget.

## Why the project is not another generic self-improvement loop

The project explicitly concedes that learning from failed trajectories, synthetic curricula, and adaptive sampling already exist. Its narrower contribution is longitudinal: stable mechanism identity across policy updates, transition-aware budget allocation, and measurement of whether risk is removed or merely displaced.

## What is real in the repository

- end-to-end closed loop with post-update reevaluation
- real Chromium/Playwright isolated browser execution
- observation-aware interactive-model contract plus optional OpenAI Responses / Anthropic Messages adapters tested offline via injected clients
- failure clustering and globally optimal cross-round mechanism matching
- split/merge topology and extinct/contracting/persistent/expanding/emergent states
- equal verified-data budget baselines
- leakage gates, negative controls, repeated trials, paired inference
- matching ambiguity plus human-calibration packet/scorer
- benchmark split fingerprints and SHA-256 identity
- measured usage/cost coverage that distinguishes unknown from zero
- claim-to-evidence release audit
- retained null/adverse toy results

## What is deliberately not claimed

No released experiment establishes frontier-model superiority, production reliability improvement, or human-validated mechanism matching. Those require the paper-scale real-agent study.

## The hiring signal

The strongest signal is not feature count. It is the sequence of research decisions: prior-art audit -> narrower falsifiable question -> implementation -> discovery and disclosure of benchmark flaws -> controlled comparison -> adverse-result retention -> evidence/provenance hardening -> real-model-ready interface.

## The next decisive experiment

Replace the local reference policy with a real trainable/API-backed computer-use model, use held-out browser/desktop environment families, run 5+ training seeds and repeated trials, collect independent human mechanism labels, and test whether SORELIA reduces persistent/expanding risk without compensating emergent risk under equal verified-data and optimization budgets.
