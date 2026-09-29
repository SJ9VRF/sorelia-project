from __future__ import annotations
from copy import deepcopy
from pathlib import Path
from typing import Dict
import json, yaml
from .experiments import run_mode
from .run_manifest import build_run_manifest, write_run_manifest


def run_ablations(config_path: str, out_path: str) -> Dict:
    cfg = yaml.safe_load(Path(config_path).read_text())
    variants = {}

    variants['full'] = ('sorelia', deepcopy(cfg))
    variants['static_priority'] = ('priority', deepcopy(cfg))

    noexp = deepcopy(cfg)
    noexp.setdefault('curriculum', {})['exploration_ratio'] = 0.0
    variants['no_exploration'] = ('sorelia', noexp)

    one = deepcopy(cfg)
    one.setdefault('sorelia', {})['iterations'] = 1
    variants['single_iteration'] = ('sorelia', one)

    shuffled = deepcopy(cfg)
    shuffled['experimental_control'] = 'shuffled_failure_labels'
    variants['shuffled_failure_labels'] = ('sorelia', shuffled)

    random_clusters = deepcopy(cfg)
    random_clusters['experimental_control'] = 'random_cluster_assignment'
    variants['random_cluster_assignment'] = ('sorelia', random_clusters)

    raw = {}
    summary = {}
    for name, (mode, local) in variants.items():
        rows = run_mode(local, mode)
        raw[name] = rows
        final = rows[-1]
        summary[name] = {
            'mode': mode,
            'iterations': int(local['sorelia']['iterations']),
            'exploration_ratio': float(local['curriculum']['exploration_ratio']),
            'task_success_rate': final.get('task_success_rate'),
            'stress_task_success_rate': final.get('stress_task_success_rate'),
            'failures_per_task': final.get('failures_per_task'),
            'stress_failures_per_task': final.get('stress_failures_per_task'),
            'catastrophic_action_rate': final.get('catastrophic_action_rate'),
            'exact_eval_leakage': final.get('exact_eval_leakage'),
            'experimental_control': final.get('experimental_control', 'none'),
        }
    result = {'summary': summary, 'raw': raw}
    out = Path(out_path); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding='utf-8')
    write_run_manifest(out.with_suffix(out.suffix + '.manifest.json'),
                       build_run_manifest(config_path, 'core-ablations', {'variants': sorted(variants)}))
    return result
