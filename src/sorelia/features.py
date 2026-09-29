from __future__ import annotations
import numpy as np
from .schema import TASK_FAMILIES, FAILURE_TYPES, Task

PERT_KEYS = ["layout", "wording", "hidden_state", "noise", "delay", "interruption"]
ACTIONS = ["A", "B", "C", "D"]


def task_features(task: Task) -> np.ndarray:
    fam = [1.0 if task.family == x else 0.0 for x in TASK_FAMILIES]
    fail = [1.0 if task.failure_mode == x else 0.0 for x in FAILURE_TYPES]
    pert = [float(task.perturbation.get(k, 0.0)) for k in PERT_KEYS]
    return np.array(fam + fail + [float(task.difficulty), float(task.horizon) / 10.0] + pert, dtype=float)


def _teacher_weights(dim: int) -> np.ndarray:
    # Fixed deterministic linear teacher. This makes the sandbox genuinely learnable
    # while retaining interactions between task semantics and action choice.
    i = np.arange(4 * dim, dtype=float).reshape(4, dim)
    return np.sin(i * 0.73 + 0.2) + 0.55 * np.cos(i * 0.31 + 0.7)


def correct_action(task: Task, step: int) -> str:
    x = np.concatenate([task_features(task), [step / max(1, task.horizon)]])
    scores = _teacher_weights(len(x)) @ x
    return ACTIONS[int(np.argmax(scores))]
