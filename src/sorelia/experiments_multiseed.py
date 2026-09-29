from __future__ import annotations
from copy import deepcopy
from pathlib import Path
from typing import Dict, List
import json
import yaml
import numpy as np
from .experiments import MODES, run_mode
from .analysis.statistics import bootstrap_mean_ci, paired_bootstrap_delta, paired_permutation_test
from .run_manifest import build_run_manifest, write_run_manifest


def run_multiseed(config_path: str, out_path: str) -> Dict:
    cfg = yaml.safe_load(Path(config_path).read_text())
    seeds = list(cfg.get("experiment", {}).get("seeds", [0, 1, 2, 3, 4]))
    raw: List[Dict] = []
    for seed in seeds:
        local = deepcopy(cfg)
        local["seed"] = int(seed)
        for mode in MODES:
            for row in run_mode(local, mode):
                raw.append({"seed": int(seed), **row})

    final_iteration = int(cfg["sorelia"]["iterations"])
    summary = {}
    for mode in MODES:
        finals = [r for r in raw if r["mode"] == mode and r["iteration"] == final_iteration]
        summary[mode] = {}
        for metric in ["task_success_rate", "stress_task_success_rate", "failures_per_task", "stress_failures_per_task", "catastrophic_action_rate", "mean_steps", "mean_cost"]:
            vals = [float(r[metric]) for r in finals if r.get(metric) is not None]
            summary[mode][metric] = bootstrap_mean_ci(vals, seed=1234 + len(mode), n_boot=4000)

    pairwise = {}
    sorelia_rows = {int(r["seed"]): r for r in raw if r["mode"] == "sorelia" and r["iteration"] == final_iteration}
    for baseline in [m for m in MODES if m != "sorelia"]:
        base_rows = {int(r["seed"]): r for r in raw if r["mode"] == baseline and r["iteration"] == final_iteration}
        common = sorted(set(sorelia_rows) & set(base_rows))
        pairwise[baseline] = {}
        for metric in ["task_success_rate", "stress_task_success_rate", "failures_per_task", "stress_failures_per_task", "catastrophic_action_rate", "mean_steps", "mean_cost"]:
            a = [float(sorelia_rows[k][metric]) for k in common if sorelia_rows[k].get(metric) is not None and base_rows[k].get(metric) is not None]
            b = [float(base_rows[k][metric]) for k in common if sorelia_rows[k].get(metric) is not None and base_rows[k].get(metric) is not None]
            pairwise[baseline][metric] = {
                "paired_bootstrap": paired_bootstrap_delta(a, b, seed=2026 + len(metric) + len(baseline)),
                "paired_permutation": paired_permutation_test(a, b, seed=4040 + len(metric) + len(baseline), n_perm=10000),
            }
    result = {"seeds": seeds, "final_iteration": final_iteration, "summary": summary, "pairwise_vs_sorelia": pairwise, "raw": raw}
    out = Path(out_path); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    write_run_manifest(out.with_suffix(out.suffix + ".manifest.json"), build_run_manifest(config_path, "multiseed", {"seeds": seeds, "modes": MODES}))
    return result
