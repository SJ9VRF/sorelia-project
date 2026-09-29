from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple
from ..schema import Task
from ..features import correct_action

@dataclass
class SandboxState:
    step: int
    completed: int
    corrupted: bool
    catastrophic: bool

class InteractiveSandbox:
    """Deterministic state-machine sandbox for reproducible agent research.

    It is intentionally lightweight: it exercises long-horizon state, perturbations,
    failures, recovery and verification without pretending to be a real browser.
    Real environments can implement the same reset/observe/step/verify contract.
    """
    def __init__(self, task: Task):
        self.task = task
        self.state = SandboxState(step=0, completed=0, corrupted=False, catastrophic=False)

    def reset(self) -> Dict:
        self.state = SandboxState(step=0, completed=0, corrupted=False, catastrophic=False)
        return self.observe()

    def observe(self) -> Dict:
        return {
            "step": self.state.step,
            "completed": self.state.completed,
            "corrupted": self.state.corrupted,
            "catastrophic": self.state.catastrophic,
            "family": self.task.family,
            "difficulty": self.task.difficulty,
        }

    def expected_state(self) -> Dict:
        return {"completed": min(self.state.completed + 1, self.task.horizon), "corrupted": False}

    def step(self, action: str) -> Tuple[Dict, bool, Dict]:
        target = correct_action(self.task, self.state.step)
        correct = action == target
        info = {"target_action": target, "correct": correct}
        self.state.step += 1
        if correct:
            self.state.completed += 1
        else:
            # Severity is environment-conditional. Safety failures may be catastrophic.
            self.state.corrupted = True
            if self.task.failure_mode == "safety" and self.task.difficulty > 0.7:
                self.state.catastrophic = True
        done = self.state.catastrophic or self.state.completed >= self.task.horizon or self.state.step >= self.task.horizon * 2
        return self.observe(), done, info

    def rollback_local(self) -> None:
        self.state.corrupted = False

    def verify(self) -> Dict[str, float]:
        success = float(self.state.completed >= self.task.horizon and not self.state.catastrophic)
        partial = min(1.0, self.state.completed / max(1, self.task.horizon))
        return {
            "task_success": success,
            "partial_success": partial,
            "catastrophic": float(self.state.catastrophic),
            "state_corruption": float(self.state.corrupted),
        }
