#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${PYTHONPATH:-}:$ROOT/src"

echo "[1/5] runtime"
python -m sorelia.cli doctor

echo "[2/5] claim/evidence audit"
python -m sorelia.cli audit --root .
PYTHONPATH=src python scripts/validate_traceability.py

echo "[3/5] focused integrity tests"
python -m pytest -q tests/test_project_page.py tests/test_release_audit.py tests/test_contamination.py tests/test_negative_controls.py tests/test_metrics_usage_unknown.py

echo "[4/5] browser fixture smoke"
if python - <<'PYCHECK' >/dev/null 2>&1
import playwright
PYCHECK
then
  python scripts/run_browser_smoke.py >/tmp/sorelia_reviewer_browser.txt
  cat /tmp/sorelia_reviewer_browser.txt
else
  echo 'Playwright not installed; browser smoke skipped. Install .[browser] and run again.'
fi

echo "[5/5] evidence boundary"
printf '%s\n' \
  'Executed: local + isolated Chromium engineering evidence.' \
  'Not claimed: frontier-model superiority, production reliability, completed human calibration, or SOTA performance.' \
  'Open website/index.html and SUBMISSION_INDEX.md for the reviewer-facing entry points.'
