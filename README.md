# SORELIA

## Tracking and Training the Moving Failure Frontier of Interactive Agents

**Aura Yavary**

SORELIA is an executable research system for studying a harder problem than generic self-improvement: **how the failure frontier of an interactive agent moves after each training round, and where the next unit of training budget should be spent to reduce future risk.**

> Don’t just train on failures. Track which failures disappear, which mutate, which emerge, and train where the frontier is moving next.

### Why this framing

Prior work already shows that unsuccessful trajectories can seed self-evolving curricula, failed trajectories can be repaired at inference time, and GUI agents can improve through iterative synthetic-data loops. SORELIA therefore does **not** claim that “learning from failure” itself is novel. Its research target is longitudinal failure-frontier optimization under a fixed verified-data budget.

### Core loop

`evaluate → extract failures → discover mechanisms → track frontier transition → allocate risk-aware budget → generate counterfactual tasks → verify → post-train → re-evaluate → repeat`

### Moving-frontier state

Across adjacent iterations, each stable failure mechanism is classified as:

- **extinct** — observed before, absent now
- **contracting** — risk mass fell materially
- **persistent** — remains roughly stable
- **expanding** — risk mass grew materially
- **emergent** — newly observed after the update

SORELIA uses this transition state in curriculum allocation so training budget follows the moving reliability boundary rather than the static frequency histogram.

### Defensible research hypothesis

Under equal verified-data and optimization budgets, a curriculum that tracks failure-frontier dynamics should reduce persistent/expanding risk more efficiently than random, difficulty-only, static failure-frequency, or static failure-priority curricula—without simply shifting error mass into new failure mechanisms.

### What is implemented

- long-horizon task/trial/trajectory logging across six application families and eight failure types
- real Chromium/Playwright isolated browser backend plus local deterministic sandbox
- structured failure events, recovery events, state-based grading and safety metadata
- mechanism-oriented failure clustering, centroid signatures and cluster-coherence diagnostics
- globally optimal stable mechanism matching across policy iterations, including split/merge topology events
- extinction, emergence, expansion, contraction and persistence classification plus risk-displacement measurement
- frontier-risk metrics and transition artifacts
- moving-frontier curriculum allocation with exploration reserve
- equal-budget random, difficulty, human-balanced and failure-frequency baselines
- counterfactual task mutation, solvability verification, duplicate rejection and provenance
- correction/preference data builders and cumulative supervised post-training
- repeated-trial, multi-seed evaluation; bootstrap intervals; paired randomization tests; recurrence, distribution-shift, risk-displacement and topology metrics
- exact train/eval contamination gates plus near-duplicate diagnostics
- executable shuffled-failure-label and random-cluster negative controls
- human matching-calibration packet export, inter-annotator agreement, and matcher-vs-human scoring utilities
- tests, CI, reproducibility docs, paper scaffold, dataset card, novelty audit and truth audit
- observation-aware provider-agnostic model contract, deterministic replay adapter, and optional OpenAI Responses / Anthropic Messages adapters tested with injected offline clients
- immutable benchmark split manifests with task fingerprints and split SHA-256 digests
- runtime `doctor` command separating core, browser, provider-SDK and credential readiness without exposing secrets

### Evidence policy

Committed numerical results are engineering smoke tests, not claims about frontier computer-use models. No SOTA or production-scale result is claimed until the paper-scale gates in `docs/PAPER_READINESS.md` are satisfied.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest -q
sorelia doctor
sorelia run --config configs/smoke.yaml --out artifacts/smoke
sorelia compare --config configs/smoke.yaml --out artifacts/comparison.json
sorelia multiseed --config configs/paper_smoke.yaml --out artifacts/paper_smoke/multiseed.json
```

For offline source-tree execution, where build dependencies cannot be downloaded:

```bash
PYTHONPATH=src python -m pytest -q tests
PYTHONPATH=src python -m sorelia.cli run --config configs/smoke.yaml --out artifacts/smoke
PYTHONPATH=src python scripts/run_multiseed.py --config configs/paper_smoke.yaml --out artifacts/paper_smoke/multiseed.json
```

## Measured usage, not invented cost

Provider-backed decisions can return measured token usage and model-call latency through `AgentDecision`. Cost is reported only when an explicit estimator is supplied. Local agents therefore show `usage_coverage=0` / `cost_coverage=0` and `mean_cost=null` rather than fabricated token counts or zero-dollar cost. See `docs/USAGE_ACCOUNTING.md` and `docs/PROVIDER_INTEGRATION.md`.


## Public project artifacts

- `website/index.html` — 14-section flagship project page for a ~60-second first read.
- `website/demo.html` — interactive retained Chromium trajectory replay.
- `website/assets/sorelia-demo.mp4` — short evidence-grounded trajectory-replay video; not a fabricated screen recording.
- `website/assets/architecture.svg` — closed-loop system architecture figure.
- `website/assets/failure-frontier.svg` — retained risk-displacement measurement figure.
- `website/assets/project-card.png` — portfolio/social project card.
- `docs/INTERVIEW_TALK_TRACKS.md` — 30s / 60s / 5m explanation and hard-question answers.
- `docs/DEMO_NARRATION.md` — public demo narration.
- `docs/PROJECT_CARD.md` — copy for the main portfolio homepage.

## Research questions

1. Does failure-conditioned curriculum allocation improve held-out performance per verified training trajectory?
2. Does it reduce recurrence of targeted failure mechanisms rather than merely memorizing generated tasks?
3. Does improvement transfer to held-out perturbations, task instances, failure variants and environment families?
4. Which failures have the highest learning value: frequent, severe, recoverable, uncertain, or broadly transferable failures?
5. When does iterative self-generated training become unstable, narrow the data distribution, or create new failure modes?

## Main comparison

Every method receives the same base agent, training method, synthetic-task budget, evaluation tasks and number of iterations. The required curricula are random synthetic, static difficulty, manually balanced, failure-frequency, static failure-priority and adaptive SORELIA. The local harness now executes shuffled-label and random-cluster negative controls; paper-scale evaluation additionally requires unrelated-failure controls, real-agent data-path ablations, and a learned UCB/bandit allocator.

## Scientific claim gate

All numeric artifacts committed here are **engineering smoke tests**. They validate that the experimental harness executes, records mixed/null outcomes, and can compute uncertainty. They are not claims about real computer-use agents. Real claims require the gate in `docs/RELEASE_STATUS.md` and `docs/PAPER_READINESS.md`.

The five-seed synthetic smoke test, for example, does not show universal dominance: SORELIA and random tie on mean final task success in this toy setting, while other metrics differ. That is retained rather than optimized away because the purpose of this artifact is credible research infrastructure.

## Current engineering evidence

The committed local experiments are deliberately adversarial to the project narrative: null and adverse runs are retained, negative controls execute, and the release does not claim SORELIA superiority. The purpose of the local evidence is to establish that the harness is executable, falsifiable, leakage-gated, and uncertainty-aware. See `docs/CURRENT_RESULTS.md` and `docs/TRUTH_AUDIT.md`. Historical release corrections remain in `CHANGELOG.md`.

## Repository map

```text
src/sorelia/
  agents/              trainable local policy
  analysis/            bootstrap/statistical and failure-shift analysis
  adapters/            production backend boundary
  benchmarks/          task generator + executable local sandbox
  clustering/          failure representation and grouping
  curriculum/          adaptive, UCB and baseline allocators
  data/                JSONL I/O
  evals/               task/reliability/cost metrics
  generation/          counterfactual generation + verification
  infra/               rollout engine
  safety/              action-risk utilities
  training/            SFT examples + preference/correction records
  pipeline.py          complete SORELIA execution
  experiments.py       equal-budget curriculum comparison
  experiments_multiseed.py
configs/
docs/
paper/
scripts/
tests/
website/
artifacts/
```


## Five-minute audit path

If you are reviewing the project quickly, read these in order:

1. `docs/FIVE_MINUTE_TOUR.md`
2. `docs/NOVELTY_AUDIT.md`
3. `docs/FAILURE_FRONTIER_SPEC.md`
4. `src/sorelia/analysis/frontier.py`
5. `src/sorelia/curriculum/scheduler.py`
6. `docs/TRUTH_AUDIT.md`
7. `docs/RESULTS_V090_INTEGRITY.md`
8. `docs/MODEL_ADAPTER_CONTRACT.md`
9. `docs/BENCHMARK_IDENTITY.md`

The longitudinal analysis does not assume a coarse `(family, failure_type)` key is a stable mechanism. Discovered cluster signatures are matched across policy versions with globally optimal bipartite assignment, stable IDs are inherited, and split/merge topology events are recorded.

## Production replacement boundary

`InteractiveSandbox` is the fastest executable reference environment. `PlaywrightEnvironmentAdapter` is also executable against an isolated local HTML fixture using a real Chromium DOM/action loop. An external-site or desktop backend should implement the same `reset/observe/expected_state/step/verify/rollback_local` contract in an isolated context. Model adapters consume an observation-aware `DecisionContext` containing the current observation, expected state, bounded recent actions/observations, and task metadata. `CallableInteractiveAgent` provides a provider-agnostic boundary for API-backed or local VLM/LLM policies without coupling provider SDKs to the evaluation core. This keeps the research question and experimental controls unchanged when moving from local smoke tests to Playwright/desktop and trainable VLM policies.


## Evidence-linked release discipline

Every public claim is mapped to concrete repository artifacts in `docs/CLAIM_EVIDENCE_REGISTRY.json`. `sorelia audit --root .` fails if supported claims lose evidence files or unsupported SOTA language leaks into public-facing artifacts. End-to-end runs write a configuration hash, source-tree hash, platform/Python metadata and an evidence index so a reviewer can identify exactly which code/config produced an artifact.

## Reproducibility and integrity

Generated examples record origin failure/cluster, generation iteration and version, mutation signature and verifier version. Core grading is state-based. Main experiments use held-out evaluation tasks and fixed synthetic-data budgets. Tests and source compilation are part of CI. The release includes a checksum manifest.

## Status

**v1.7.0 release candidate:** public-release validation, source tests, claim/evidence audit, and reviewer paths are gated. See `docs/RELEASE_STATUS.md` and `docs/CURRENT_RESULTS.md` for measured status. The benchmark now includes an executable static failure-priority baseline, deterministic shifted/stress evaluation, matching-confidence diagnostics, exact train/eval contamination gates, executable shuffled-label and random-cluster negative controls, and a human matching-calibration packet/scorer.  Cross-round failure identity uses globally optimal gated bipartite matching rather than greedy assignment; evaluation uses repeated trials per task; multiseed comparisons include paired bootstrap intervals and paired randomization tests. The fixed-budget comparison executes the moving-frontier scheduler, enforces identical verified-data budgets, writes run manifests/evidence indexes, and passes the claim-to-evidence audit.


The local system is executable end to end and tested, including a real Chromium/Playwright fixture backend. External frontier-model training and uncontrolled external-site/desktop evaluation are intentionally not claimed as executed because they require model/browser/GPU resources outside this artifact environment. See `docs/RELEASE_STATUS.md` for the exact boundary and `docs/EXPERIMENTS.md` for the paper-scale execution matrix.


## Current integrity controls

The current release enforces train/eval leakage gates, executable shuffled-label and random-cluster negative controls, longitudinal matching-confidence diagnostics, blank human-calibration packet export, and claim-to-evidence auditing. Human judgments are **not** synthesized; completed human calibration remains a paper-scale gate. See `docs/CURRENT_RESULTS.md`, `docs/CONTAMINATION_PROTOCOL.md`, and `docs/HUMAN_CALIBRATION_PROTOCOL.md`.

## Flagship project page

The standalone reviewer-facing project page is `website/index.html`. It is structured for a ~60-second first read and includes the problem, novelty, architecture, author contribution, experiments, evidence-tiered results, failure analysis, interactive trajectory demo, scaling, safety/limitations, technical deep dive, artifacts, and citation. `website/demo.html` replays a retained Chromium fixture rather than a fabricated marketing trajectory.

## Public-repository governance

- `CONTRIBUTING.md` — evidence-first contribution rules.
- `SECURITY.md` — sandbox/credential/high-risk-action boundary.
- `CODE_OF_CONDUCT.md` — rigorous and respectful research conduct.
- `docs/BENCHMARK_CARD.md` — intended benchmark scope and limitations.
- `docs/SYSTEM_CARD.md` — system components, intended use, and out-of-scope claims.
- `docs/EXPERIMENT_REGISTRY.md` — executed vs pending experiment ledger.
- `docs/DECISION_LOG.md` — key research choices and rejected shortcuts.
- `docs/REVIEWER_REPRODUCTION.md` — static, fast, and full reproduction paths.
- `scripts/reviewer_demo.sh` — one-command reviewer integrity/demo path.

## Evidence Layer

SORELIA intentionally exposes the research process rather than presenting a perfect retrospective. Start here:

- [Experiment journal](docs/EXPERIMENT_JOURNAL.md) — nine executed experiment families with hypothesis, setup, result, interpretation, and next decision.
- [What did not work](docs/FAILED_EXPERIMENTS.md) — failed hypotheses, regressions, methodological corrections, and what changed.
- [Decision log](docs/DECISION_LOG.md) — Decision → Alternatives → Evidence → Trade-off → Outcome.
- [Unexpected findings](docs/UNEXPECTED_FINDINGS.md) — observations that changed the research direction.
- [Raw artifact index](docs/RAW_ARTIFACT_INDEX.md) — curated eval runs, failures, configs, ablations, plots, and qualitative cases.
- [Research-process page](website/evidence.html) — the public evidence layer beneath the polished project page.

The archive did not contain historical Git metadata before v1.5.0. No backdated history is fabricated; real Git history begins with an explicit baseline import and ships as a portable bundle.

## Research traceability

The Evidence Layer is audit-oriented, not just narrative. Start with:

- `website/traceability.html` — four end-to-end research threads.
- `docs/TRACEABILITY_MATRIX.md` — hypothesis → experiment → failed assumption → decision → raw artifact → implementation/config → conclusion.
- `docs/EVIDENCE_LEDGER.json` — machine-readable paths and SHA-256 hashes for retained evidence and implementation files.
- `docs/RESEARCH_THREADS.md` — human-readable thread narratives.

Historical boundary: retained Git history begins from the imported v1.5.0 release candidate. Earlier methodological changes are supported by archived artifacts and notes; missing historical commits are not reconstructed.
