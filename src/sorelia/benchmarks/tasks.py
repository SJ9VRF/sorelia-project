from __future__ import annotations
import random
from typing import List
from ..schema import Task, TASK_FAMILIES, FAILURE_TYPES

PERT_KEYS = ["layout", "wording", "hidden_state", "noise", "delay", "interruption"]

def make_tasks(n: int, seed: int = 0, prefix: str = "rb") -> List[Task]:
    rng = random.Random(seed)
    tasks = []
    for i in range(n):
        family = TASK_FAMILIES[i % len(TASK_FAMILIES)]
        failure = FAILURE_TYPES[(i * 3 + seed) % len(FAILURE_TYPES)]
        difficulty = round(0.25 + 0.7 * rng.random(), 3)
        horizon = rng.randint(3, 7)
        pert = {k: round(rng.random() * 0.8, 3) for k in PERT_KEYS}
        tasks.append(Task(
            task_id=f"{prefix}-{i:04d}", family=family, failure_mode=failure,
            difficulty=difficulty, horizon=horizon, perturbation=pert,
            instruction=f"Complete a {family} task robust to {failure} failures.", seed=seed * 10000 + i,
        ))
    return tasks


def make_shifted_tasks(n: int, seed: int = 0, prefix: str = "stress") -> List[Task]:
    """Construct a deterministic harder/OOD evaluation split.

    The stress split shifts difficulty, horizon and perturbation intensity while
    preserving the task/failure vocabulary. It is intentionally simple but gives
    the harness an executable distribution-shift check rather than claiming
    generalization from an IID split alone.
    """
    rng = random.Random(seed)
    tasks = []
    for i in range(n):
        family = TASK_FAMILIES[(i * 2 + 1) % len(TASK_FAMILIES)]
        failure = FAILURE_TYPES[(i * 5 + seed + 1) % len(FAILURE_TYPES)]
        difficulty = round(0.65 + 0.34 * rng.random(), 3)
        horizon = rng.randint(6, 10)
        pert = {k: round(0.55 + rng.random() * 0.45, 3) for k in PERT_KEYS}
        tasks.append(Task(
            task_id=f"{prefix}-{i:04d}", family=family, failure_mode=failure,
            difficulty=difficulty, horizon=horizon, perturbation=pert,
            instruction=f"Complete a shifted {family} task robust to {failure} failures.",
            seed=seed * 10000 + 500000 + i,
        ))
    return tasks
