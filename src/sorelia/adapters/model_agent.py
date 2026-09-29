from __future__ import annotations
from dataclasses import asdict
from typing import Callable, Mapping, Any
from ..schema import DecisionContext

DecisionFn = Callable[[Mapping[str, Any]], str]

class CallableInteractiveAgent:
    """Provider-agnostic adapter for a real interactive model backend.

    `decision_fn` receives a JSON-serializable dictionary containing the task,
    current observation, expected state, and bounded recent history, and returns
    one environment action string. This keeps provider SDKs outside core eval code.
    """
    def __init__(self, decision_fn: DecisionFn, *, model_id: str, version: str):
        self.decision_fn = decision_fn
        self.model_id = model_id
        self.version = version

    def act(self, context: DecisionContext) -> str:
        payload = {
            "task": asdict(context.task),
            "step": context.step,
            "observation": context.observation,
            "expected_state": context.expected_state,
            "recent_actions": context.recent_actions,
            "recent_observations": context.recent_observations,
            "deterministic": context.deterministic,
        }
        action = self.decision_fn(payload)
        if not isinstance(action, str) or not action.strip():
            raise ValueError("decision_fn must return a non-empty action string")
        return action.strip()


class ReplayInteractiveAgent:
    """Deterministic adapter for replaying audited action sequences."""
    def __init__(self, actions: list[str], *, model_id: str = "replay_agent", version: str = "replay-v1"):
        self.actions = list(actions)
        self.model_id = model_id
        self.version = version
        self._cursor = 0

    def act(self, context: DecisionContext) -> str:
        if self._cursor >= len(self.actions):
            raise IndexError("replay action sequence exhausted")
        action = self.actions[self._cursor]
        self._cursor += 1
        return action
