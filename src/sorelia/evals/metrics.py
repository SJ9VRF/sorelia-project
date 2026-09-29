from __future__ import annotations
from collections import Counter
from typing import Dict, List
import numpy as np
from ..schema import Trajectory


def compute_metrics(trajs: List[Trajectory]) -> Dict:
    if not trajs:
        return {}
    fails = [f for t in trajs for f in t.failure_events]
    recs = [r for t in trajs for r in t.recovery_events]
    successes = np.asarray([float(t.success) for t in trajs])
    first_failure = []
    corrupt = []
    propagation = []
    for t in trajs:
        if t.failure_events:
            first_failure.append(t.failure_events[0].step / max(1, t.num_steps))
            propagation.extend(f.downstream_effects for f in t.failure_events)
        corrupt.append(float(t.grader_results.get("state_corruption", 0.0)))
    known_cost = [t for t in trajs if t.cost_known]
    known_usage = [t for t in trajs if t.usage_known]
    total_cost = float(np.sum([t.monetary_cost for t in known_cost])) if known_cost else None
    successful_known_cost = [t for t in known_cost if t.success]
    return {
        "n_tasks": len(trajs),
        "task_success_rate": float(successes.mean()),
        "mean_partial_success": float(np.mean([t.partial_success for t in trajs])),
        "mean_steps": float(np.mean([t.num_steps for t in trajs])),
        "mean_latency_ms": float(np.mean([t.latency_ms for t in trajs])),
        "mean_model_latency_ms": float(np.mean([t.model_latency_ms for t in known_usage])) if known_usage else None,
        "usage_coverage": float(len(known_usage) / len(trajs)),
        "cost_coverage": float(len(known_cost) / len(trajs)),
        "mean_input_tokens": float(np.mean([t.input_tokens for t in known_usage])) if known_usage else None,
        "mean_output_tokens": float(np.mean([t.output_tokens for t in known_usage])) if known_usage else None,
        "mean_cost": float(np.mean([t.monetary_cost for t in known_cost])) if known_cost else None,
        "cost_per_success": float(total_cost / len(successful_known_cost)) if successful_known_cost else None,
        "failure_events": len(fails),
        "failures_per_task": float(len(fails)/len(trajs)),
        "first_failure_position": float(np.mean(first_failure)) if first_failure else None,
        "error_propagation_depth": float(np.mean(propagation)) if propagation else 0.0,
        "state_corruption_rate": float(np.mean(corrupt)),
        "recovery_attempts": len(recs),
        "recovery_success_rate": float(np.mean([r.success for r in recs])) if recs else 0.0,
        "catastrophic_action_rate": float(np.mean([t.grader_results.get("catastrophic", 0) for t in trajs])),
        "failure_type_counts": dict(Counter(f.failure_type for f in fails)),
    }
