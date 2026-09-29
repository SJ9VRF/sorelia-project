from __future__ import annotations
from typing import Dict
import math


def priority_score(cluster: Dict, total_failures: int, uncertainty: float = 0.5, generalization: float = 0.5) -> float:
    frequency = cluster["size"] / max(1, total_failures)
    severity = cluster["severity"]
    learnability = cluster["recoverability"]
    return frequency * (0.5 + severity) * (0.5 + learnability) * (0.75 + uncertainty) * (0.75 + generalization)


def allocate(cluster_summary: Dict[int, Dict], budget: int, exploration_ratio: float = 0.2) -> Dict[int, int]:
    if not cluster_summary or budget <= 0:
        return {}
    total_failures = sum(v["size"] for v in cluster_summary.values())
    scores = {k: priority_score(v, total_failures) for k, v in cluster_summary.items()}
    exploit = int(round(budget * (1 - exploration_ratio)))
    explore = budget - exploit
    ssum = sum(scores.values()) or 1.0
    alloc = {k: int(math.floor(exploit * scores[k] / ssum)) for k in scores}
    used = sum(alloc.values())
    # deterministic remainder
    for k in sorted(scores, key=scores.get, reverse=True):
        if used >= exploit: break
        alloc[k] += 1; used += 1
    keys = sorted(scores)
    i = 0
    while explore > 0:
        alloc[keys[i % len(keys)]] += 1
        i += 1; explore -= 1
    return alloc


def frontier_priority_score(cluster: Dict, total_failures: int, status: str = "persistent", uncertainty: float = 0.5, generalization: float = 0.5) -> float:
    """Prioritize the moving failure frontier, not failure frequency alone.

    Expanding/emergent mechanisms get extra budget; contracting mechanisms are
    down-weighted; extinct mechanisms get zero exploitation budget.
    """
    base = priority_score(cluster, total_failures, uncertainty, generalization)
    multiplier = {
        "emergent": 1.45,
        "expanding": 1.35,
        "persistent": 1.0,
        "contracting": 0.55,
        "extinct": 0.0,
        "unknown": 1.0,
    }.get(status, 1.0)
    return base * multiplier


def allocate_frontier(cluster_summary: Dict[int, Dict], budget: int, status_by_cluster: Dict[int, str] | None = None, exploration_ratio: float = 0.2) -> Dict[int, int]:
    if not cluster_summary or budget <= 0:
        return {}
    status_by_cluster = status_by_cluster or {}
    total_failures = sum(v["size"] for v in cluster_summary.values())
    scores = {}
    for cid, c in cluster_summary.items():
        status = status_by_cluster.get(cid, "unknown")
        scores[cid] = frontier_priority_score(c, total_failures, status=status)
    exploit = int(round(budget * (1 - exploration_ratio)))
    explore = budget - exploit
    ssum = sum(scores.values())
    if ssum <= 0:
        # all known mechanisms are extinct: spend budget on exploration instead.
        explore = budget
        exploit = 0
        ssum = 1.0
    alloc = {k: int(math.floor(exploit * scores[k] / ssum)) for k in scores}
    used = sum(alloc.values())
    for k in sorted(scores, key=scores.get, reverse=True):
        if used >= exploit:
            break
        alloc[k] += 1
        used += 1
    keys = sorted(scores)
    i = 0
    while explore > 0:
        alloc[keys[i % len(keys)]] += 1
        i += 1
        explore -= 1
    return alloc
