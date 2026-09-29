from __future__ import annotations
from typing import Dict, List
from ..schema import Task, TASK_FAMILIES, FAILURE_TYPES
from ..benchmarks.tasks import make_tasks
from ..generation.generator import generate_from_clusters


def random_curriculum(budget: int, iteration: int, seed: int) -> List[Task]:
    return make_tasks(budget, seed=seed + 2000 * iteration, prefix=f"random-i{iteration}")


def human_balanced_curriculum(budget: int, iteration: int, seed: int) -> List[Task]:
    # Explicitly balanced across task families and failure modes; no feedback from observed failures.
    tasks = make_tasks(budget, seed=seed + 3000 * iteration, prefix=f"human-i{iteration}")
    for i, t in enumerate(tasks):
        t.family = TASK_FAMILIES[i % len(TASK_FAMILIES)]
        t.failure_mode = FAILURE_TYPES[(i // len(TASK_FAMILIES)) % len(FAILURE_TYPES)]
        t.difficulty = min(.95, .35 + .10 * iteration + (i % 5) * .08)
    return tasks


def difficulty_curriculum(budget: int, iteration: int, seed: int) -> List[Task]:
    tasks = make_tasks(budget, seed=seed + 4000 * iteration, prefix=f"difficulty-i{iteration}")
    center = min(.9, .30 + .18 * iteration)
    for i, t in enumerate(tasks):
        t.difficulty = max(.1, min(.98, center + ((i % 7) - 3) * .04))
    return tasks


def frequency_allocation(cluster_summary: Dict[int, Dict], budget: int) -> Dict[int, int]:
    if not cluster_summary: return {}
    total = sum(v["size"] for v in cluster_summary.values()) or 1
    alloc = {k: int(budget * v["size"] / total) for k, v in cluster_summary.items()}
    used = sum(alloc.values())
    for k in sorted(cluster_summary, key=lambda x: cluster_summary[x]["size"], reverse=True):
        if used >= budget: break
        alloc[k] += 1; used += 1
    return alloc
