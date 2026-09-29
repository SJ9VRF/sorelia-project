#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
# This rehearsal is intentionally heavier than the fast release gate.
python -m sorelia.cli run --config configs/v090_release.yaml --out artifacts/paper_rehearsal/run
python -m sorelia.cli compare --config configs/v090_release.yaml --out artifacts/paper_rehearsal/compare.json
python -m sorelia.cli ablate --config configs/v090_release.yaml --out artifacts/paper_rehearsal/ablations.json
python -m sorelia.cli multiseed --config configs/v090_release.yaml --out artifacts/paper_rehearsal/multiseed.json
