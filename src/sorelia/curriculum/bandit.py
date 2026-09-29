from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict
import math

@dataclass
class UCBAllocator:
    """Research scheduler that allocates curriculum budget using observed downstream gain.

    Each failure cluster is treated as an arm. update() consumes measured held-out gain
    attributed to examples sourced from that cluster. Allocation uses UCB1 plus an
    explicit exploration reserve, so the policy cannot collapse to a single cluster.
    """
    counts: Dict[int, int] = field(default_factory=dict)
    values: Dict[int, float] = field(default_factory=dict)

    def score(self, cluster_id: int, prior: float = 0.0) -> float:
        n = self.counts.get(cluster_id, 0)
        if n == 0:
            return float("inf")
        total = max(1, sum(self.counts.values()))
        return self.values.get(cluster_id, 0.0) + math.sqrt(2.0 * math.log(total + 1) / n) + 0.1 * prior

    def allocate(self, summary: Dict[int, Dict], budget: int, exploration_ratio: float = .2) -> Dict[int, int]:
        if not summary or budget <= 0:
            return {}
        out = {k: 0 for k in summary}
        explore = min(budget, max(len(summary), int(round(budget * exploration_ratio))))
        keys = sorted(summary)
        for i in range(explore):
            out[keys[i % len(keys)]] += 1
        for _ in range(budget - explore):
            cid = max(keys, key=lambda k: self.score(k, prior=float(summary[k].get("severity", 0.0))))
            out[cid] += 1
            self.counts[cid] = self.counts.get(cid, 0) + 1
        return out

    def update(self, cluster_id: int, observed_gain: float, weight: int = 1) -> None:
        old_n = self.counts.get(cluster_id, 0)
        old_v = self.values.get(cluster_id, 0.0)
        new_n = old_n + max(1, weight)
        self.values[cluster_id] = (old_v * old_n + observed_gain * max(1, weight)) / new_n
        self.counts[cluster_id] = new_n
