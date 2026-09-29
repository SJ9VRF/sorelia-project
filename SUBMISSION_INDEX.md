# SORELIA — submission index

**Aura Yavary**  
**SORELIA: Tracking and Training the Moving Failure Frontier of Interactive Agents**

## 60-second review path
1. `website/index.html` — flagship project page.
2. `website/assets/sorelia-demo.mp4` — 20.8s evidence-grounded trajectory replay.
3. `paper/main.pdf` — research manuscript with architecture and failure-frontier figures.
4. `docs/EXECUTIVE_REVIEW.md` — concise scientific/engineering review.
5. `docs/NOVELTY_AUDIT.md` — prior-work boundary and claims deliberately not made.
6. `docs/CURRENT_RESULTS.md` — canonical current evidence and scientific claim boundary.

## Technical audit path
1. `docs/FAILURE_FRONTIER_SPEC.md`
2. `src/sorelia/analysis/frontier.py`
3. `src/sorelia/curriculum/scheduler.py`
4. `src/sorelia/pipeline.py`
5. `tests/`
6. `docs/CLAIM_EVIDENCE_REGISTRY.json`

## Interview material
- `docs/INTERVIEW_TALK_TRACKS.md`
- `docs/DEMO_NARRATION.md`
- `docs/RESUME_BULLETS.md`
- `docs/PROJECT_CARD.md`

## Visual assets
- `website/assets/architecture.svg`
- `website/assets/failure-frontier.svg`
- `website/assets/project-card.png`

## Reproduce
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest -q
sorelia audit --root .
bash scripts/reproduce_release.sh
```

## Evidence boundary
The public release proves an executable and falsifiable research system, including local/Chromium interaction, longitudinal failure tracking, fixed-budget comparisons, contamination controls, negative controls, statistics, provider boundaries and provenance. It does **not** claim frontier-model superiority, production reliability, completed human calibration, or SOTA performance.

## Public-repository audit
- `docs/BENCHMARK_CARD.md`
- `docs/SYSTEM_CARD.md`
- `docs/EXPERIMENT_REGISTRY.md`
- `docs/DECISION_LOG.md`
- `docs/REVIEWER_REPRODUCTION.md`
- `CONTRIBUTING.md`
- `SECURITY.md`

## Additional public cards
- `docs/MODEL_CARD.md`
- `docs/DATA_CARD.md`
- `docs/RELEASE_CANDIDATE_CHECKLIST.md`

## Containerized review
```bash
docker build -t sorelia-review .
docker run --rm sorelia-review
```

## Evidence Layer
- `website/evidence.html`
- `docs/EXPERIMENT_JOURNAL.md`
- `docs/FAILED_EXPERIMENTS.md`
- `docs/UNEXPECTED_FINDINGS.md`
- `docs/DECISION_LOG.md`
- `docs/RAW_ARTIFACT_INDEX.md`
- `artifacts/git_history/`
