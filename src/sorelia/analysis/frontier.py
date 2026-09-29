from __future__ import annotations
from collections import defaultdict
from typing import Dict, Iterable, Tuple, Any
import numpy as np
from scipy.optimize import linear_sum_assignment
from ..schema import Trajectory

Mechanism = Tuple[str, str]


def _risk(size: int, total: int, severity: float, recoverability: float) -> float:
    prevalence = float(size) / max(1, total)
    return prevalence * (0.5 + float(severity)) * (1.5 - float(recoverability))


def _cosine(a, b) -> float:
    a = np.asarray(a, dtype=float); b = np.asarray(b, dtype=float)
    d = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.dot(a, b) / d) if d > 0 else 0.0


def mechanism_profile(trajectories: Iterable[Trajectory]) -> Dict[Mechanism, Dict[str, float]]:
    """Coarse taxonomy profile retained for compatibility and aggregate reporting."""
    counts = defaultdict(int); sev = defaultdict(float); rec = defaultdict(float); n_traj = 0
    for tr in trajectories:
        n_traj += 1
        for f in tr.failure_events:
            key = (tr.task_family, f.failure_type)
            counts[key] += 1; sev[key] += float(f.severity); rec[key] += float(f.recoverability)
    out: Dict[Mechanism, Dict[str, float]] = {}
    denom = max(1, n_traj)
    for key, n in counts.items():
        severity = sev[key] / n; recoverability = rec[key] / n; prevalence = n / denom
        out[key] = {"count": float(n), "prevalence": float(prevalence), "severity": float(severity),
                    "recoverability": float(recoverability),
                    "risk": float(prevalence * (0.5 + severity) * (1.5 - recoverability))}
    return out


def frontier_transition(before: Iterable[Trajectory], after: Iterable[Trajectory], ratio: float = 0.20) -> Dict[str, object]:
    """Coarse transition report over taxonomy keys. Prefer cluster_frontier_transition for paper analyses."""
    b = mechanism_profile(before); a = mechanism_profile(after); keys = sorted(set(b) | set(a))
    rows = []; counts = defaultdict(int)
    for key in keys:
        br = float(b.get(key, {}).get("risk", 0.0)); ar = float(a.get(key, {}).get("risk", 0.0))
        if br > 0 and ar == 0: status = "extinct"
        elif br == 0 and ar > 0: status = "emergent"
        elif br == 0 and ar == 0: status = "absent"
        else:
            delta_ratio = (ar - br) / max(br, 1e-12)
            status = "expanding" if delta_ratio > ratio else "contracting" if delta_ratio < -ratio else "persistent"
        counts[status] += 1
        rows.append({"family": key[0], "failure_type": key[1], "status": status,
                     "risk_before": br, "risk_after": ar, "risk_delta": ar - br,
                     "count_before": int(b.get(key, {}).get("count", 0)),
                     "count_after": int(a.get(key, {}).get("count", 0))})
    return {"summary": dict(counts), "risk_before": float(sum(x.get("risk", 0.0) for x in b.values())),
            "risk_after": float(sum(x.get("risk", 0.0) for x in a.values())), "mechanisms": rows}


def cluster_frontier_transition(before: Dict[int, Dict[str, Any]], after: Dict[int, Dict[str, Any]],
                                iteration: int, match_threshold: float = 0.78,
                                event_threshold: float = 0.70, ratio: float = 0.20) -> Dict[str, Any]:
    """Track discovered failure mechanisms across training rounds using cluster signatures.

    Unlike taxonomy-only matching, this follows sub-mechanisms within the same family/type.
    Greedy one-to-one matching establishes identity; secondary high-similarity edges expose
    splits/merges. Stable IDs are inherited across rounds and new IDs are minted only for
    genuinely emergent mechanisms.
    """
    before = {int(k): dict(v) for k, v in before.items()}; after = {int(k): dict(v) for k, v in after.items()}
    btot = sum(int(v.get("size", 0)) for v in before.values()); atot = sum(int(v.get("size", 0)) for v in after.values())
    for cid, c in before.items():
        c.setdefault("stable_id", f"m{max(0, iteration-1)}_{cid}")
    for c in before.values():
        c["risk"] = _risk(c.get("size", 0), btot, c.get("severity", 0), c.get("recoverability", 0))
    for c in after.values():
        c["risk"] = _risk(c.get("size", 0), atot, c.get("severity", 0), c.get("recoverability", 0))

    candidates = []
    all_edges = []
    for bi, bc in before.items():
        for ai, ac in after.items():
            sim = _cosine(bc.get("centroid", []), ac.get("centroid", []))
            # Small semantic bonus makes identity robust when continuous features drift.
            if bc.get("family") == ac.get("family"): sim += 0.04
            if bc.get("failure_type") == ac.get("failure_type"): sim += 0.04
            sim = min(1.0, sim)
            all_edges.append((sim, bi, ai))
            if sim >= match_threshold: candidates.append((sim, bi, ai))

    matched_b = set(); matched_a = set(); primary = []
    # Globally optimal one-to-one identity matching. Greedy matching can make locally
    # attractive assignments that reduce total semantic consistency across rounds.
    b_ids = sorted(before); a_ids = sorted(after)
    if b_ids and a_ids:
        sim_matrix = np.zeros((len(b_ids), len(a_ids)), dtype=float)
        for i, bi in enumerate(b_ids):
            for j, ai in enumerate(a_ids):
                bc, ac = before[bi], after[ai]
                sim = _cosine(bc.get("centroid", []), ac.get("centroid", []))
                if bc.get("family") == ac.get("family"): sim += 0.04
                if bc.get("failure_type") == ac.get("failure_type"): sim += 0.04
                sim_matrix[i, j] = min(1.0, sim)
        rows_i, cols_j = linear_sum_assignment(-sim_matrix)
        for i, j in zip(rows_i.tolist(), cols_j.tolist()):
            sim = float(sim_matrix[i, j]); bi, ai = b_ids[i], a_ids[j]
            if sim >= match_threshold:
                matched_b.add(bi); matched_a.add(ai); primary.append((sim, bi, ai))

    rows = []; status_by_cluster = {}; stable_id_by_cluster = {}; counts = defaultdict(int)
    removed_risk = 0.0; introduced_risk = 0.0
    match_diagnostics = []
    for sim, bi, ai in primary:
        bc, ac = before[bi], after[ai]; br, ar = float(bc["risk"]), float(ac["risk"])
        # Confidence margin against the strongest alternative assignment touching either endpoint.
        alternatives = [s for s,b,a in all_edges if (b == bi or a == ai) and not (b == bi and a == ai)]
        runner_up = max(alternatives) if alternatives else 0.0
        margin = float(sim - runner_up)
        delta_ratio = (ar - br) / max(br, 1e-12)
        status = "expanding" if delta_ratio > ratio else "contracting" if delta_ratio < -ratio else "persistent"
        sid = str(bc["stable_id"]); ac["stable_id"] = sid
        status_by_cluster[ai] = status; stable_id_by_cluster[ai] = sid; counts[status] += 1
        if ar < br: removed_risk += br - ar
        elif ar > br: introduced_risk += ar - br
        rows.append({"stable_id": sid, "before_cluster": bi, "after_cluster": ai, "similarity": sim,
                     "match_margin": margin, "family": ac.get("family"), "failure_type": ac.get("failure_type"), "status": status,
                     "risk_before": br, "risk_after": ar, "risk_delta": ar - br})
        match_diagnostics.append({"stable_id": sid, "similarity": float(sim), "margin": margin,
                                  "ambiguous": bool(margin < 0.05)})

    for bi, bc in before.items():
        if bi in matched_b: continue
        br = float(bc["risk"]); removed_risk += br; counts["extinct"] += 1
        rows.append({"stable_id": bc["stable_id"], "before_cluster": bi, "after_cluster": None, "similarity": 0.0,
                     "family": bc.get("family"), "failure_type": bc.get("failure_type"), "status": "extinct",
                     "risk_before": br, "risk_after": 0.0, "risk_delta": -br})

    for ai, ac in after.items():
        if ai in matched_a: continue
        ar = float(ac["risk"]); introduced_risk += ar; counts["emergent"] += 1
        sid = f"m{iteration}_{ai}"; ac["stable_id"] = sid
        status_by_cluster[ai] = "emergent"; stable_id_by_cluster[ai] = sid
        rows.append({"stable_id": sid, "before_cluster": None, "after_cluster": ai, "similarity": 0.0,
                     "family": ac.get("family"), "failure_type": ac.get("failure_type"), "status": "emergent",
                     "risk_before": 0.0, "risk_after": ar, "risk_delta": ar})

    # Detect topology changes independently of primary identity matching.
    strong = [(s,b,a) for s,b,a in all_edges if s >= event_threshold]
    out_by_b = defaultdict(list); in_by_a = defaultdict(list)
    for s,b,a in strong: out_by_b[b].append((a,s)); in_by_a[a].append((b,s))
    events = []
    for b, xs in out_by_b.items():
        if len(xs) > 1:
            events.append({"event": "split", "source_cluster": b, "targets": [a for a,_ in sorted(xs)],
                           "stable_id": before[b].get("stable_id")})
    for a, xs in in_by_a.items():
        if len(xs) > 1:
            events.append({"event": "merge", "target_cluster": a, "sources": [b for b,_ in sorted(xs)],
                           "stable_id": after[a].get("stable_id")})

    rb = float(sum(c["risk"] for c in before.values())); ra = float(sum(c["risk"] for c in after.values()))
    displacement = introduced_risk / max(removed_risk, 1e-12) if removed_risk > 0 else (float("inf") if introduced_risk > 0 else 0.0)
    md_sims = [x["similarity"] for x in match_diagnostics]
    md_margins = [x["margin"] for x in match_diagnostics]
    calibration = {
        "matched": len(match_diagnostics),
        "mean_similarity": float(np.mean(md_sims)) if md_sims else None,
        "mean_margin": float(np.mean(md_margins)) if md_margins else None,
        "ambiguous_matches": int(sum(x["ambiguous"] for x in match_diagnostics)),
        "ambiguous_rate": float(np.mean([x["ambiguous"] for x in match_diagnostics])) if match_diagnostics else 0.0,
    }
    return {"summary": dict(counts), "risk_before": rb, "risk_after": ra, "net_risk_change": ra-rb,
            "risk_removed": float(removed_risk), "risk_introduced": float(introduced_risk),
            "risk_displacement_ratio": float(displacement), "mechanisms": rows, "topology_events": events,
            "matching_calibration": calibration,
            "status_by_cluster": {str(k): v for k,v in status_by_cluster.items()},
            "stable_id_by_cluster": {str(k): v for k,v in stable_id_by_cluster.items()},
            "annotated_after": after}


def status_index(report: Dict[str, object]) -> Dict[Mechanism, str]:
    return {(row["family"], row["failure_type"]): row["status"] for row in report.get("mechanisms", []) if row.get("after_cluster") is not None}


def cluster_status_index(report: Dict[str, Any]) -> Dict[int, str]:
    return {int(k): v for k, v in report.get("status_by_cluster", {}).items()}
