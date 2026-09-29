# Research decision log

Each decision uses the same format: **Decision → Alternatives → Evidence → Trade-off → Outcome**.

## D1 — Narrow the novelty claim
**Decision:** Do not claim novelty for “learning from failure”; focus on longitudinal failure-frontier dynamics and risk displacement.

**Alternatives:** Keep the original failure-driven curriculum framing; market synthetic task generation as the central contribution.

**Evidence:** Literature audit found prior failure-driven/self-improving agent curricula.

**Trade-off:** The new claim is narrower and harder to prove, but substantially more defensible.

**Outcome:** SORELIA was renamed/reframed around moving failure-frontier tracking.

## D2 — Track mechanisms, not coarse labels
**Decision:** Use cluster signatures and globally optimal gated matching across rounds.

**Alternatives:** `(task family, failure type)` keys; greedy nearest-cluster matching.

**Evidence:** Coarse keys merge distinct mechanisms; greedy matching can create globally inconsistent assignments.

**Trade-off:** More implementation complexity and a new ambiguity-calibration problem.

**Outcome:** Stable mechanism IDs, margins, split/merge events, and human-calibration packets.

## D3 — Equalize verified-data budgets
**Decision:** Give compared curricula the same verified training-data budget.

**Alternatives:** Let each generator keep all accepted examples; compare at fixed wall-clock.

**Evidence:** Otherwise “better curriculum” can simply mean “more data.”

**Trade-off:** May underuse a productive generator, but makes causal interpretation cleaner.

**Outcome:** Budget equality is asserted in the comparison contract and tests.

## D4 — Verify before training
**Decision:** Generated tasks must pass executable/state-based verification before entering the training set.

**Alternatives:** Train on all generated trajectories; rely only on an LLM quality judge.

**Evidence:** The project treats unverifiable synthetic tasks as a contamination/noise risk.

**Trade-off:** Lower data yield and extra verifier engineering.

**Outcome:** Generated-task lineage records accepted/rejected status and verifier version.

## D5 — Preserve adverse and null outcomes
**Decision:** Keep runs where SORELIA loses.

**Alternatives:** Tune the toy environment until the flagship method wins; report only best seeds.

**Evidence:** Static-priority, human-balanced, frequency, and random-cluster controls sometimes outperform SORELIA.

**Trade-off:** Less impressive headline numbers, much stronger credibility.

**Outcome:** Negative controls and non-winning tables remain in the public artifact.

## D6 — Unknown usage is not zero
**Decision:** Report unknown token/cost metrics as `null` with coverage fractions.

**Alternatives:** Fixed synthetic token counts; hard-coded provider pricing; treat missing as zero.

**Evidence:** Early fixed accounting created false precision.

**Trade-off:** Some tables are incomplete.

**Outcome:** `usage_coverage` and `cost_coverage` are first-class metrics.

## D7 — Infrastructure errors are not agent failures
**Decision:** Provider/network/parser failures abort or flag infrastructure state.

**Alternatives:** Convert them into ordinary task failures.

**Evidence:** Mixing infrastructure faults into the taxonomy corrupts the scientific failure distribution.

**Trade-off:** Fewer usable trajectories when infrastructure is unstable.

**Outcome:** Provider adapters use strict parsing and rollout cleanup.

## D8 — Human calibration is a required gate
**Decision:** Do not treat automatic mechanism matches as validated ground truth.

**Alternatives:** Use similarity score alone; manually inspect only cherry-picked examples.

**Evidence:** Retained runs include 25%+ ambiguous-match rates.

**Trade-off:** Full scientific claim requires independent annotation effort.

**Outcome:** Blank annotation packets, Cohen’s κ scorer, matcher-vs-human metrics, and explicit pending status.
