from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from ..schema import Trajectory, FAILURE_TYPES, TASK_FAMILIES

@dataclass
class FailurePoint:
    failure_id: str
    trajectory_id: str
    family: str
    failure_type: str
    severity: float
    recoverability: float
    difficulty: float
    step_fraction: float


def extract_failure_points(trajectories: List[Trajectory]) -> List[FailurePoint]:
    out = []
    for tr in trajectories:
        for j, fe in enumerate(tr.failure_events):
            out.append(FailurePoint(
                failure_id=f"{tr.trajectory_id}:{j}", trajectory_id=tr.trajectory_id,
                family=tr.task_family, failure_type=fe.failure_type,
                severity=fe.severity, recoverability=fe.recoverability,
                difficulty=float(fe.previous_state.get("difficulty", .5)),
                step_fraction=fe.step / max(1, tr.num_steps),
            ))
    return out


def embed(points: List[FailurePoint]) -> np.ndarray:
    rows = []
    for p in points:
        fam = [1.0 if p.family == x else 0.0 for x in TASK_FAMILIES]
        typ = [1.0 if p.failure_type == x else 0.0 for x in FAILURE_TYPES]
        rows.append(fam + typ + [p.severity, p.recoverability, p.difficulty, p.step_fraction])
    return np.asarray(rows, dtype=float)


def cluster(points: List[FailurePoint], k: int = 8, seed: int = 0) -> Tuple[np.ndarray, Dict]:
    if not points:
        return np.array([], dtype=int), {"k": 0, "silhouette": None}
    X = embed(points)
    k = max(1, min(k, len(points)))
    if k == 1:
        labels = np.zeros(len(points), dtype=int)
        sil = None
    else:
        km = KMeans(n_clusters=k, random_state=seed, n_init=10)
        labels = km.fit_predict(X)
        sil = float(silhouette_score(X, labels)) if len(set(labels)) > 1 and len(points) > k else None
    return labels, {"k": k, "silhouette": sil}


def summarize(points: List[FailurePoint], labels: np.ndarray) -> Dict[int, Dict]:
    groups = defaultdict(list)
    for p, lab in zip(points, labels):
        groups[int(lab)].append(p)
    summary = {}
    for lab, ps in groups.items():
        ft = Counter(p.failure_type for p in ps).most_common(1)[0][0]
        fam = Counter(p.family for p in ps).most_common(1)[0][0]
        X = embed(ps)
        summary[lab] = {
            "size": len(ps), "failure_type": ft, "family": fam,
            "severity": float(np.mean([p.severity for p in ps])),
            "recoverability": float(np.mean([p.recoverability for p in ps])),
            "difficulty": float(np.mean([p.difficulty for p in ps])),
            "step_fraction": float(np.mean([p.step_fraction for p in ps])),
            "centroid": np.mean(X, axis=0).astype(float).tolist(),
            "failure_ids": [p.failure_id for p in ps],
            "family_entropy": float(-sum((n/len(ps))*np.log2(n/len(ps)) for n in Counter(p.family for p in ps).values())),
            "type_entropy": float(-sum((n/len(ps))*np.log2(n/len(ps)) for n in Counter(p.failure_type for p in ps).values())),
        }
    return summary
