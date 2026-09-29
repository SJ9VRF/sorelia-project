# Reviewer reproduction guide

## 2-minute static audit

1. `SUBMISSION_INDEX.md`
2. `website/index.html`
3. `docs/EXECUTIVE_REVIEW.md`
4. `docs/NOVELTY_AUDIT.md`
5. `docs/TRUTH_AUDIT.md`

## Fast executable gate

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest -q
sorelia doctor
sorelia audit --root .
```

## Reviewer demo

```bash
bash scripts/reviewer_demo.sh
```

This runs the lightweight integrity path and prints the exact evidence boundary. It is not the paper-scale experiment.

## Full release reproduction

```bash
bash scripts/reproduce_release.sh
```

## Paper-scale rehearsal

```bash
bash scripts/rehearse_paper_protocol.sh
```

The rehearsal specifies the intended matrix; external model/GPU/browser resources remain required for the actual paper-scale study.
