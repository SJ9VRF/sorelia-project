#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q
python -m compileall -q src
python -m sorelia.cli audit --root .
PYTHONPATH=src python scripts/validate_traceability.py
python -m sorelia.cli doctor >/tmp/sorelia_v130_doctor.json
rm -rf artifacts/release_repro
python -m sorelia.cli run --config configs/release_gate.yaml --out artifacts/release_repro >/tmp/sorelia_v130_run.json
python -m sorelia.cli compare --config configs/release_gate.yaml --out artifacts/release_repro_compare.json >/tmp/sorelia_v130_compare.json
python -m sorelia.cli ablate --config configs/release_gate.yaml --out artifacts/release_repro_ablations.json >/tmp/sorelia_v130_ablations.json
python - <<'PY'
import json
from pathlib import Path

doctor=json.loads(Path('/tmp/sorelia_v130_doctor.json').read_text())
assert doctor['ok_core'] is True

manifest=json.loads(Path('artifacts/release_repro/benchmark_manifest.json').read_text())
assert manifest['splits']['train']['count'] > 0
assert manifest['splits']['eval']['count'] > 0
assert manifest['splits']['train']['sha256'] != manifest['splits']['eval']['sha256']

rows=json.loads(Path('artifacts/release_repro_compare.json').read_text())
by={}
for r in rows:
    if r['iteration']>0:
        assert r['verified_training_tasks_this_iteration'] > 0
        assert r.get('exact_eval_leakage', 0) == 0
        by.setdefault(r['iteration'], set()).add(r['verified_training_tasks_this_iteration'])
assert all(len(v)==1 for v in by.values()), by
sorelia=[r for r in rows if r['mode']=='sorelia' and r['iteration']>=2]
assert sorelia and all(r['frontier_summary'] for r in sorelia)

abl=json.loads(Path('artifacts/release_repro_ablations.json').read_text())['summary']
required={'full','static_priority','no_exploration','single_iteration','shuffled_failure_labels','random_cluster_assignment'}
assert required <= set(abl), set(abl)
assert all((v.get('exact_eval_leakage') in (0, None)) for v in abl.values())

packets=list(Path('artifacts/release_repro').glob('matching_annotation_packet_i*.jsonl'))
assert packets, 'missing matching calibration packet'
metrics=json.loads(Path('artifacts/release_repro/metrics.json').read_text())
assert all(r.get('exact_eval_leakage',0)==0 for r in metrics if r['iteration']>0)
# Local PolicyAgent does not report provider usage; unknown must remain unknown, not fake zero-cost evidence.
assert all(r.get('usage_coverage') == 0.0 for r in metrics)
assert all(r.get('cost_coverage') == 0.0 for r in metrics)
assert all(r.get('mean_cost') is None for r in metrics)
print('SORELIA v1.4.0 release reproduction checks passed')
PY
