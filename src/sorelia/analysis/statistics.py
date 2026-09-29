from __future__ import annotations
from collections import Counter
from typing import Dict, Iterable, List, Sequence, Tuple
import numpy as np
from ..schema import Trajectory


def bootstrap_mean_ci(values: Sequence[float], seed: int = 0, n_boot: int = 2000, alpha: float = .05) -> Dict[str, float]:
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return {"mean": float("nan"), "ci_low": float("nan"), "ci_high": float("nan"), "n": 0}
    rng = np.random.default_rng(seed)
    samples = rng.choice(arr, size=(n_boot, len(arr)), replace=True).mean(axis=1)
    return {
        "mean": float(arr.mean()),
        "ci_low": float(np.quantile(samples, alpha / 2)),
        "ci_high": float(np.quantile(samples, 1 - alpha / 2)),
        "n": int(len(arr)),
    }


def failure_distribution(trajs: Iterable[Trajectory]) -> Dict[str, float]:
    counts = Counter(f.failure_type for t in trajs for f in t.failure_events)
    total = sum(counts.values())
    return {k: v / total for k, v in sorted(counts.items())} if total else {}


def js_divergence(p: Dict[str, float], q: Dict[str, float]) -> float:
    keys = sorted(set(p) | set(q))
    if not keys:
        return 0.0
    a = np.asarray([p.get(k, 0.0) for k in keys], dtype=float)
    b = np.asarray([q.get(k, 0.0) for k in keys], dtype=float)
    m = .5 * (a + b)
    def kl(x, y):
        mask = x > 0
        return float(np.sum(x[mask] * np.log2(x[mask] / y[mask])))
    return .5 * kl(a, m) + .5 * kl(b, m)


def recurrence_rate(before: Iterable[Trajectory], after: Iterable[Trajectory]) -> float:
    b = Counter(f.failure_type for t in before for f in t.failure_events)
    a = Counter(f.failure_type for t in after for f in t.failure_events)
    if not b:
        return 0.0
    recurring = sum(min(v, a.get(k, 0)) for k, v in b.items())
    return float(recurring / sum(b.values()))


def paired_success_delta(before: List[Trajectory], after: List[Trajectory], seed: int = 0) -> Dict[str, float]:
    b = {t.task_id: float(t.success) for t in before}
    a = {t.task_id: float(t.success) for t in after}
    keys = sorted(set(b) & set(a))
    vals = [a[k] - b[k] for k in keys]
    return bootstrap_mean_ci(vals, seed=seed)


def paired_permutation_test(a: Sequence[float], b: Sequence[float], seed: int = 0, n_perm: int = 20_000) -> Dict[str, float]:
    """Two-sided paired randomization test for matched task/seed outcomes."""
    x = np.asarray(a, dtype=float); y = np.asarray(b, dtype=float)
    if x.shape != y.shape or x.size == 0:
        return {"mean_delta": float("nan"), "p_value": float("nan"), "n": int(min(x.size, y.size))}
    d = x - y; obs = abs(float(d.mean()))
    rng = np.random.default_rng(seed)
    ge = 0
    for _ in range(int(n_perm)):
        signs = rng.choice(np.asarray([-1.0, 1.0]), size=d.size)
        if abs(float((d * signs).mean())) >= obs - 1e-15:
            ge += 1
    return {"mean_delta": float(d.mean()), "p_value": float((ge + 1) / (n_perm + 1)), "n": int(d.size)}


def paired_bootstrap_delta(a: Sequence[float], b: Sequence[float], seed: int = 0, n_boot: int = 10_000, alpha: float = .05) -> Dict[str, float]:
    x = np.asarray(a, dtype=float); y = np.asarray(b, dtype=float)
    if x.shape != y.shape or x.size == 0:
        return {"mean_delta": float("nan"), "ci_low": float("nan"), "ci_high": float("nan"), "n": int(min(x.size, y.size))}
    d = x - y; rng = np.random.default_rng(seed)
    idx = rng.integers(0, d.size, size=(int(n_boot), d.size))
    means = d[idx].mean(axis=1)
    return {"mean_delta": float(d.mean()), "ci_low": float(np.quantile(means, alpha/2)),
            "ci_high": float(np.quantile(means, 1-alpha/2)), "n": int(d.size)}
