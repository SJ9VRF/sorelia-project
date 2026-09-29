from __future__ import annotations
import hashlib, json, math, re
from typing import Dict, Iterable, List, Tuple
from ..schema import Task


def _norm_text(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def semantic_fingerprint(task: Task) -> str:
    """Exact content fingerprint excluding IDs, seeds and provenance-only fields."""
    payload = {
        "family": task.family,
        "failure_mode": task.failure_mode,
        "difficulty": round(float(task.difficulty), 6),
        "horizon": int(task.horizon),
        "perturbation": {k: round(float(v), 6) for k, v in sorted(task.perturbation.items())},
        "instruction": _norm_text(task.instruction),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def _distance(a: Task, b: Task) -> float:
    """Normalized structural distance in [0, ~1+] for near-duplicate diagnostics."""
    if a.family != b.family or a.failure_mode != b.failure_mode:
        return float("inf")
    keys = sorted(set(a.perturbation) | set(b.perturbation))
    p = math.sqrt(sum((float(a.perturbation.get(k, 0.0)) - float(b.perturbation.get(k, 0.0))) ** 2 for k in keys))
    p /= max(1.0, math.sqrt(len(keys)))
    d = abs(float(a.difficulty) - float(b.difficulty))
    h = abs(int(a.horizon) - int(b.horizon)) / 20.0
    return float(0.65 * p + 0.20 * d + 0.15 * h)


def contamination_report(training: Iterable[Task], evaluation: Iterable[Task], near_threshold: float = 0.06) -> Dict[str, object]:
    train = list(training); evals = list(evaluation)
    train_ids = {t.task_id for t in train}; eval_ids = {t.task_id for t in evals}
    id_overlap = sorted(train_ids & eval_ids)

    tf = {}
    for t in train: tf.setdefault(semantic_fingerprint(t), []).append(t.task_id)
    ef = {}
    for t in evals: ef.setdefault(semantic_fingerprint(t), []).append(t.task_id)
    exact_hashes = sorted(set(tf) & set(ef))

    near: List[Dict[str, object]] = []
    # Small local benchmark: exhaustive check is deliberate and deterministic.
    for t in train:
        for e in evals:
            dist = _distance(t, e)
            if dist <= near_threshold:
                near.append({"train_task": t.task_id, "eval_task": e.task_id, "distance": round(dist, 8)})
    denom = max(1, len(train) * len(evals))
    return {
        "train_tasks": len(train),
        "eval_tasks": len(evals),
        "task_id_overlap_count": len(id_overlap),
        "task_id_overlap": id_overlap,
        "exact_semantic_overlap_count": len(exact_hashes),
        "exact_semantic_overlap_hashes": exact_hashes,
        "near_duplicate_pairs": near,
        "near_duplicate_pair_count": len(near),
        "near_duplicate_pair_rate": float(len(near) / denom),
        "near_threshold": float(near_threshold),
        "passes_exact_leakage_gate": len(id_overlap) == 0 and len(exact_hashes) == 0,
    }


def assert_no_exact_leakage(training: Iterable[Task], evaluation: Iterable[Task]) -> Dict[str, object]:
    report = contamination_report(training, evaluation)
    if not report["passes_exact_leakage_gate"]:
        raise AssertionError(f"train/eval contamination detected: {report}")
    return report
