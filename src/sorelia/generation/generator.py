from __future__ import annotations
import hashlib
import json
import random
from typing import Dict, List
from ..schema import Task

PERT_KEYS = ["layout", "wording", "hidden_state", "noise", "delay", "interruption"]
GENERATOR_VERSION = "counterfactual_v2"

def _signature(family: str, failure_type: str, perturbation: Dict[str, float], horizon: int) -> str:
    payload = json.dumps({"family": family, "failure": failure_type, "perturbation": perturbation, "horizon": horizon}, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]

def generate_from_clusters(cluster_summary: Dict[int, Dict], allocation: Dict[int, int], iteration: int, seed: int = 0) -> List[Task]:
    rng = random.Random(seed + iteration * 1009)
    tasks = []
    idx = 0
    for cid, n in sorted(allocation.items()):
        c = cluster_summary[cid]
        source_ids = list(c.get("failure_ids", []))
        for j in range(n):
            pert = {k: round(rng.random(), 3) for k in PERT_KEYS}
            difficulty = min(.98, max(.15, c["difficulty"] + rng.uniform(-.2, .2)))
            horizon = rng.randint(3, 8)
            source_failure = source_ids[j % len(source_ids)] if source_ids else None
            tasks.append(Task(
                task_id=f"gen-i{iteration}-c{cid}-{idx:05d}",
                family=c["family"], failure_mode=c["failure_type"],
                difficulty=round(difficulty, 3), horizon=horizon,
                perturbation=pert,
                instruction=f"Counterfactual variant targeting {c['failure_type']} in {c['family']}.",
                seed=seed * 100000 + iteration * 10000 + idx,
                source_failure_id=source_failure,
                source_cluster=cid,
                generation_iteration=iteration,
                generator_version=GENERATOR_VERSION,
                mutation_signature=_signature(c["family"], c["failure_type"], pert, horizon),
            ))
            idx += 1
    return tasks
