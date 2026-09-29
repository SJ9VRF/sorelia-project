from __future__ import annotations
import numpy as np
from typing import List, Tuple
from ..schema import Task
from ..features import ACTIONS, correct_action


def supervised_examples(agent, tasks: List[Task]) -> Tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for t in tasks:
        for step in range(t.horizon):
            X.append(agent.features_for(t, step))
            y.append(ACTIONS.index(correct_action(t, step)))
    return np.asarray(X, dtype=float), np.asarray(y, dtype=int)
