## 1.6.0 - Evidence Layer and real-from-now-on research history

- Added a curated experiment journal with nine executed experiment families.
- Added explicit failed-hypothesis / invalidated-assumption records and unexpected findings.
- Rewrote the decision log into Decision → Alternatives → Evidence → Trade-off → Outcome format.
- Added curated raw eval, failure, ablation, config, qualitative-case and plot directories.
- Added a public `website/evidence.html` and a lower-page “Inside the research process” layer on the flagship homepage.
- Started real Git history from the available v1.5.0 archive baseline; no historical commits were backfilled.
- Added public-release contract checks for the Evidence Layer.

## 1.5.0 - final hiring-readiness release candidate

- Added a canonical current-evidence page and removed stale historical framing from the main README.
- Added model/policy card, release-candidate checklist, Dockerfile, devcontainer, and optional Chromium browser-smoke CI.
- Added a public-release validator for required artifacts, version consistency, placeholders, local Markdown links, and non-empty public assets.
- Added validator contract test and Makefile `public-audit` / `release-candidate` targets.
- Re-ran the full source suite, claim/evidence audit, public-release validator, and reviewer demo on the final source snapshot.
- Preserved the distinction between a successful Chromium fixture smoke and unavailable Playwright-managed screenshot rendering in this runtime.

## 1.4.0 - public repository governance and reviewer reproduction

- Added contribution, security, code-of-conduct, benchmark/system cards, experiment registry, research decision log, reviewer reproduction guide, GitHub templates, and one-command reviewer demo.
- Cleaned public release structure and retained explicit executed-vs-pending experiment boundaries.

## 1.3.0 - hiring artifact stack

- Added architecture/failure-frontier visuals, evidence-grounded trajectory video, project card, interview talk tracks, résumé wording, and submission index.
- Embedded the core figures in the paper and activated evidence-backed project-page artifacts.

## 1.2.0 - flagship project page, interactive trajectory demo, and public artifact layer

- Rebuilt the project homepage around a 60-second hiring-manager reading path.
- Added all 14 flagship sections: hero, problem, core idea, architecture, contribution, experiments, results, failure analysis, interactive demo, scaling, safety/limitations, technical deep dive, artifacts, and citation.
- Added an interactive browser-trajectory demo derived from the retained Chromium fixture.
- Added an explicit technical report and public-facing research blog artifact.
- Preserved evidence-tier labels so engineering smoke results cannot be mistaken for frontier-model claims.
- Kept unreleased GitHub/video artifacts visibly unavailable rather than fabricating links.

## 1.1.0 - provider boundary, truthful usage accounting, and release hardening

- Added optional OpenAI Responses and Anthropic Messages adapters with lazy imports and injected-client offline tests.
- Added `AgentDecision` so providers can return measured input/output tokens, model-call latency, optional cost, and metadata.
- Removed synthetic per-action token and cost accounting from rollouts.
- Aggregate metrics now distinguish unknown from measured zero with `usage_coverage` and `cost_coverage`.
- Added `try/finally` environment cleanup for provider/backend exceptions.
- Extended `sorelia doctor` with provider SDK and credential-presence checks without exposing secrets.
- Refreshed local and Chromium smoke evidence with unknown cost represented as `null`.
- Expanded the source-tree suite to 36 passing tests and CI to Python 3.10/3.11/3.12 plus release audit/doctor gates.

## 1.0.0 - observation-aware model boundary and benchmark identity

- Added observation-aware `DecisionContext` for interactive policies.
- Added provider-agnostic `CallableInteractiveAgent` and audited replay adapter.
- Removed hard-coded rollout model identity.
- Added deterministic benchmark split manifests and task fingerprints.
- Added runtime `doctor` command and three new contract tests.
- Promoted public package/docs version to 1.0.0 without promoting toy smoke evidence to a scientific claim.

# v0.8.0

- Added executable static failure-priority baseline.
- Added deterministic shifted/stress eval split and stress metrics.
- Added cross-round matching calibration margins and ambiguity rate.
- Added executable core ablation harness.
- Added two-seed repeated-trial robustness smoke; retained non-winning SORELIA outcomes.
- Expanded tests from 18 to 22.

# Changelog

## 0.6.0

- Corrected the fixed-budget comparison so the SORELIA arm uses longitudinal moving-frontier state instead of the legacy static allocator.
- Added strict equal verified-data budget enforcement and regression tests.
- Added run manifests containing config/source hashes and runtime metadata.
- Added per-run evidence indexes.
- Added claim-to-evidence registry and `sorelia audit` release command.
- Expanded suite to 15 passing tests.
- Updated truth/release/experiment documentation to disclose the correction.


## 0.5.0
- replaced coarse taxonomy-only longitudinal tracking with centroid/signature-based stable mechanism matching
- added stable mechanism IDs across policy versions
- added split/merge failure-frontier topology events
- added risk removed, risk introduced, net risk change and risk-displacement ratio
- made curriculum allocation consume per-cluster transition state
- added two frontier-matching tests (12 total passing)
- added failure-frontier specification, five-minute reviewer tour, research brief, demo script and evidence-safe résumé wording
- reconciled release documentation with the already-executed Chromium/Playwright backend

## 0.4.0 — SORELIA research pivot

- renamed the project to **SORELIA** and standardized authorship as **Aura Yavary**
- reframed the scientific contribution from generic failure-driven curriculum learning to moving failure-frontier optimization
- added longitudinal mechanism profiles and `extinct/contracting/persistent/expanding/emergent` transition tracking
- added transition-aware curriculum allocation and frontier-risk artifacts
- added a formal novelty audit against WebRL, UI-Genie, failure-driven computer-use self-improvement, failure-aware text-agent training, learning-potential curricula and UI-Mem
- retained all smoke-test caveats; no SOTA claim added

# v0.3.0

- Replaced the Playwright placeholder with an executable Chromium-backed local browser environment.
- Added real DOM/action-loop integration testing and a browser smoke experiment.
- Added explicit evidence tiers separating browser integration from paper-scale computer-use claims.
- Generalized rollout execution via an environment factory.


## 0.2.0

- added formal Agent/Environment contracts
- added failure IDs and explicit correction-action metadata
- added generated-task lineage and verifier/generator versioning
- added mutation signatures and duplicate filtering
- added correction and trajectory preference dataset builders
- added UCB adaptive curriculum allocator
- added bootstrap confidence intervals and multi-seed runner
- added failure recurrence, Jensen-Shannon shift and paired task-delta analysis
- expanded reliability/cost metrics
- added safety action classifier
- added production browser adapter boundary documentation
- doubled test suite from four to eight passing tests
- added five-seed smoke artifact and explicit paper claim gate

## 0.1.0

Initial executable SORELIA research harness.

## v0.7.0 — optimal identity matching and repeated-trial inference

- Replaced greedy cross-round mechanism identity matching with globally optimal bipartite assignment (Hungarian algorithm) under a similarity gate.
- Added repeated evaluation trials with unique task/trial cells to avoid single-draw agent evaluation.
- Added paired bootstrap effect intervals and paired randomization tests for SORELIA-vs-baseline multiseed comparisons.
- Added regression tests for optimal matching, repeated trials, and paired statistical direction.
- Raised the release test suite from 15 to 18 tests.

## 0.9.0 - integrity, negative controls, and human-calibration infrastructure

- Added exact train/eval task-ID and semantic-fingerprint leakage gates plus near-duplicate diagnostics.
- Added executable shuffled-failure-label and random-cluster-assignment negative controls.
- Added blank matching-annotation packet export, Cohen's kappa, and matcher-vs-human scoring utilities; no human labels are fabricated.
- End-to-end runs now emit matching annotation packets and leakage diagnostics.
- Release reproduction now asserts fixed budgets, zero exact eval leakage, frontier state, negative-control execution, and calibration-packet generation.
- Added version-consistency auditing across package, README, website, and release status.
- Retained adverse toy ablation results instead of tuning the harness to make SORELIA win.

## v1.4.0 — public repository hardening
- Added contributing/security/conduct policies and research-aware GitHub templates.
- Added benchmark/system cards, experiment registry, decision log, and reviewer reproduction guide.
- Added a one-command reviewer demo with an explicit truth boundary and graceful browser-dependency handling.
- Added public-repository contract tests; 47 source-tree tests pass.
- Removed cache/build detritus from the release snapshot.
