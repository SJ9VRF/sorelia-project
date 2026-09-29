from __future__ import annotations
from dataclasses import asdict
from typing import Dict, List
from ..schema import Trajectory


def correction_records(trajs: List[Trajectory]) -> List[Dict]:
    """Step-level bad-action -> corrected-action records with auditable provenance."""
    rows = []
    for tr in trajs:
        recovery_by_step = {r.step: r for r in tr.recovery_events if r.success}
        for fe in tr.failure_events:
            if fe.step not in recovery_by_step:
                continue
            # The target action is encoded in root_cause in the local sandbox; real adapters
            # should provide explicit correction_action metadata instead.
            target = fe.root_cause.rsplit(" instead of ", 1)[-1]
            rows.append({
                "trajectory_id": tr.trajectory_id,
                "task_id": tr.task_id,
                "step": fe.step,
                "state": fe.previous_state,
                "rejected_action": fe.action,
                "chosen_action": target,
                "failure_type": fe.failure_type,
                "severity": fe.severity,
                "recoverability": fe.recoverability,
            })
    return rows


def trajectory_preferences(trajs: List[Trajectory]) -> List[Dict]:
    """Pairs successful/recovered and failed trajectories only within the same task id."""
    by_task: Dict[str, List[Trajectory]] = {}
    for tr in trajs:
        by_task.setdefault(tr.task_id, []).append(tr)
    pairs = []
    for task_id, xs in by_task.items():
        good = [x for x in xs if x.success]
        bad = [x for x in xs if not x.success]
        if good and bad:
            g = min(good, key=lambda x: (x.num_steps, x.monetary_cost))
            b = max(bad, key=lambda x: (len(x.failure_events), x.num_steps))
            pairs.append({"task_id": task_id, "chosen": g.to_dict(), "rejected": b.to_dict()})
    return pairs
