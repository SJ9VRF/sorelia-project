from __future__ import annotations
import time, uuid
from typing import Iterable, List
from dataclasses import replace
from ..schema import Task, Trajectory, FailureEvent, RecoveryEvent, DecisionContext, AgentDecision
from ..benchmarks.sandbox import InteractiveSandbox

SEVERITY = {
    "grounding": .45, "state_tracking": .6, "planning": .55, "action": .4,
    "memory": .5, "verification": .65, "recovery": .7, "safety": .95,
}
RECOVERABILITY = {
    "grounding": .85, "state_tracking": .7, "planning": .65, "action": .9,
    "memory": .75, "verification": .7, "recovery": .4, "safety": .25,
}

def run_task(agent, task: Task, allow_recovery: bool = True, env_factory=InteractiveSandbox) -> Trajectory:
    env = env_factory(task)
    tr = None
    started = time.perf_counter()
    try:
        obs = env.reset()
        tr = Trajectory(
            trajectory_id=str(uuid.uuid4()), task_id=task.task_id, task_family=task.family,
            model_id=getattr(agent, "model_id", agent.__class__.__name__), model_version=agent.version, seed=task.seed,
            initial_state=obs,
        )
        while True:
            step = int(obs["step"])
            expected = env.expected_state()
            context = DecisionContext(
                task=task,
                step=step,
                observation=dict(obs),
                expected_state=dict(expected),
                recent_actions=list(tr.actions[-8:]),
                recent_observations=list(tr.observations[-8:]),
                deterministic=False,
            )
            decision = agent.act(context)
            if isinstance(decision, AgentDecision):
                action = decision.action
                tr.input_tokens += int(decision.input_tokens)
                tr.output_tokens += int(decision.output_tokens)
                tr.tokens += int(decision.input_tokens) + int(decision.output_tokens)
                tr.model_latency_ms += float(decision.model_latency_ms)
                if decision.input_tokens or decision.output_tokens:
                    tr.usage_known = True
                if decision.monetary_cost is not None:
                    tr.monetary_cost += float(decision.monetary_cost)
                    tr.cost_known = True
            elif isinstance(decision, str):
                action = decision
            else:
                raise TypeError("agent.act must return str or AgentDecision")
            if not action.strip():
                raise ValueError("agent returned an empty action")

            nxt, done, info = env.step(action)
            tr.observations.append(obs); tr.actions.append(action)
            tr.expected_states.append(expected); tr.observed_states.append(nxt)
            if not info["correct"]:
                prev = dict(obs)
                failure = FailureEvent(
                    step=step,
                    failure_type=task.failure_mode,
                    root_cause=f"{task.failure_mode}: policy selected {action} instead of {info['target_action']}",
                    severity=SEVERITY[task.failure_mode],
                    recoverability=RECOVERABILITY[task.failure_mode],
                    previous_state=prev,
                    action=action,
                    expected_state=expected,
                    observed_state=nxt,
                    downstream_effects=1,
                    confidence=1.0,
                    failure_id=f"{tr.trajectory_id}:{len(tr.failure_events)}",
                    correction_action=info["target_action"],
                )
                tr.failure_events.append(failure)
                if allow_recovery and failure.recoverability >= .7 and not nxt["catastrophic"]:
                    env.rollback_local()
                    repaired_action = info["target_action"]
                    repaired_obs, repaired_done, repaired_info = env.step(repaired_action)
                    tr.recovery_events.append(RecoveryEvent(step=step, strategy="local_correction", success=repaired_info["correct"], extra_steps=1))
                    tr.actions.append(repaired_action)
                    tr.observed_states.append(repaired_obs)
                    tr.expected_states.append({"completed": min(nxt["completed"] + 1, task.horizon), "corrupted": False})
                    tr.observations.append(nxt)
                    nxt, done = repaired_obs, repaired_done
            obs = nxt
            if done:
                break
        grades = env.verify()
        tr.grader_results = grades
        tr.success = bool(grades["task_success"])
        tr.partial_success = grades["partial_success"]
        tr.final_state = env.observe()
        tr.num_steps = len(tr.actions)
        tr.latency_ms = (time.perf_counter() - started) * 1000
        return tr
    finally:
        if hasattr(env, "close"):
            env.close()


def run_suite(agent, tasks: Iterable[Task], allow_recovery: bool = True, env_factory=InteractiveSandbox) -> List[Trajectory]:
    return [run_task(agent, t, allow_recovery=allow_recovery, env_factory=env_factory) for t in tasks]


def run_suite_repeated(agent, tasks: Iterable[Task], trials: int = 1, seed_stride: int = 100_003, allow_recovery: bool = True, env_factory=InteractiveSandbox) -> List[Trajectory]:
    """Run repeated stochastic trials while preserving a stable base task identity.

    Each repeated task gets a unique task_id and seed so paired analyses can identify
    exact task/trial cells without conflating repeated executions.
    """
    tasks = list(tasks)
    out: List[Trajectory] = []
    for trial in range(max(1, int(trials))):
        for task in tasks:
            t = replace(task, task_id=f"{task.task_id}::trial{trial}", seed=int(task.seed) + trial * seed_stride)
            out.append(run_task(agent, t, allow_recovery=allow_recovery, env_factory=env_factory))
    return out
