from __future__ import annotations
from typing import List, Tuple
from ..schema import Task, TASK_FAMILIES, FAILURE_TYPES
from ..features import correct_action
from ..benchmarks.sandbox import InteractiveSandbox

VERIFIER_VERSION = "state_verifier_v2"

def verify_task(task: Task) -> Tuple[bool, str]:
    if task.family not in TASK_FAMILIES: return False, "invalid_family"
    if task.failure_mode not in FAILURE_TYPES: return False, "invalid_failure_mode"
    if not (1 <= task.horizon <= 20): return False, "invalid_horizon"
    if not (0 <= task.difficulty <= 1): return False, "invalid_difficulty"
    if len(task.perturbation) == 0: return False, "missing_perturbation"
    env = InteractiveSandbox(task); env.reset()
    for step in range(task.horizon):
        _, _, info = env.step(correct_action(task, step))
        if not info["correct"]: return False, "reference_policy_failed"
    grades = env.verify()
    if grades["task_success"] != 1.0: return False, "success_predicate_failed"
    if grades.get("catastrophic", 0.0) != 0.0: return False, "unsafe_reference_solution"
    task.verifier_version = VERIFIER_VERSION
    return True, "ok"


def filter_verified(tasks: List[Task]):
    kept, rejected = [], []
    seen = set()
    for t in tasks:
        if t.mutation_signature and t.mutation_signature in seen:
            rejected.append((t, "duplicate_mutation")); continue
        ok, reason = verify_task(t)
        if ok:
            kept.append(t)
            if t.mutation_signature: seen.add(t.mutation_signature)
        else:
            rejected.append((t, reason))
    return kept, rejected
