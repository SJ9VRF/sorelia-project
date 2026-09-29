from __future__ import annotations
import numpy as np
import hashlib
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from ..features import ACTIONS, task_features
from ..schema import Task, DecisionContext

class PolicyAgent:
    """Small trainable policy used to make the full research loop locally executable."""
    def __init__(self, seed: int = 0, version: str = "v0"):
        self.seed = seed
        self.model_id = "local_sgd_policy"
        self.version = version
        self.rng = np.random.default_rng(seed)
        self.model = make_pipeline(
            StandardScaler(),
            SGDClassifier(loss="log_loss", random_state=seed, max_iter=2000, tol=1e-4)
        )
        self.is_fit = False
        self.step_prior = np.array([0.05, -0.03, 0.02, -0.01])

    def _x(self, task: Task, step: int) -> np.ndarray:
        return np.concatenate([task_features(task), [step / max(1, task.horizon)]])

    def act(self, context: DecisionContext) -> str:
        task, step, deterministic = context.task, context.step, context.deterministic
        if self.is_fit:
            probs = self.model.predict_proba([self._x(task, step)])[0]
            # map classes into all actions safely
            p = np.full(len(ACTIONS), 1e-6)
            for cls, prob in zip(self.model.classes_, probs):
                p[int(cls)] = prob
            p = p / p.sum()
        else:
            # Deliberately imperfect structured prior; creates meaningful failures.
            logits = self.step_prior.copy()
            stable = int(hashlib.sha256((task.family + ":" + task.failure_mode).encode()).hexdigest()[:8], 16)
            base = (stable + task.seed + step) % 4
            logits[base] += 0.7 - 0.8 * task.difficulty
            p = np.exp(logits - logits.max()); p = p / p.sum()
        idx = int(np.argmax(p)) if deterministic else int(self.rng.choice(len(ACTIONS), p=p))
        return ACTIONS[idx]

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        self.model.fit(X, y)
        self.is_fit = True

    def features_for(self, task: Task, step: int) -> np.ndarray:
        return self._x(task, step)
