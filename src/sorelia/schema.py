from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import json

FAILURE_TYPES = [
    "grounding", "state_tracking", "planning", "action",
    "memory", "verification", "recovery", "safety"
]
TASK_FAMILIES = ["browser", "documents", "spreadsheet", "email", "files", "multi_app"]


@dataclass
class DecisionContext:
    """Observation-aware decision input for interactive agents.

    This is intentionally provider-agnostic: a local policy, VLM, API-backed agent,
    or replay policy can consume the same contract without changing the rollout engine.
    """
    task: "Task"
    step: int
    observation: Dict[str, Any]
    expected_state: Dict[str, Any]
    recent_actions: List[str] = field(default_factory=list)
    recent_observations: List[Dict[str, Any]] = field(default_factory=list)
    deterministic: bool = False


@dataclass
class AgentDecision:
    """One model decision plus optional measured usage.

    Usage fields are measurements, never estimates. Provider adapters leave cost unknown
    unless an explicit cost estimator is supplied. Local/replay agents may return a bare
    action string; rollout then records usage as unavailable rather than inventing tokens.
    """
    action: str
    input_tokens: int = 0
    output_tokens: int = 0
    model_latency_ms: float = 0.0
    monetary_cost: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FailureEvent:
    step: int
    failure_type: str
    root_cause: str
    severity: float
    recoverability: float
    previous_state: Dict[str, Any]
    action: str
    expected_state: Dict[str, Any]
    observed_state: Dict[str, Any]
    downstream_effects: int = 0
    confidence: float = 1.0
    failure_id: Optional[str] = None
    correction_action: Optional[str] = None

@dataclass
class RecoveryEvent:
    step: int
    strategy: str
    success: bool
    extra_steps: int

@dataclass
class Task:
    task_id: str
    family: str
    failure_mode: str
    difficulty: float
    horizon: int
    perturbation: Dict[str, float]
    instruction: str
    seed: int
    source_failure_id: Optional[str] = None
    source_cluster: Optional[int] = None
    generation_iteration: Optional[int] = None
    generator_version: Optional[str] = None
    mutation_signature: Optional[str] = None
    verifier_version: Optional[str] = None

@dataclass
class Trajectory:
    trajectory_id: str
    task_id: str
    task_family: str
    model_id: str
    model_version: str
    seed: int
    initial_state: Dict[str, Any]
    observations: List[Dict[str, Any]] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    expected_states: List[Dict[str, Any]] = field(default_factory=list)
    observed_states: List[Dict[str, Any]] = field(default_factory=list)
    final_state: Dict[str, Any] = field(default_factory=dict)
    success: bool = False
    partial_success: float = 0.0
    failure_events: List[FailureEvent] = field(default_factory=list)
    recovery_events: List[RecoveryEvent] = field(default_factory=list)
    grader_results: Dict[str, float] = field(default_factory=dict)
    tokens: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    usage_known: bool = False
    model_latency_ms: float = 0.0
    latency_ms: float = 0.0
    monetary_cost: float = 0.0
    cost_known: bool = False
    num_steps: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)
