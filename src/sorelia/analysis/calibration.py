from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence

LABELS = ("same", "different", "uncertain")


def build_matching_annotation_packet(frontier_report: Mapping[str, object]) -> List[Dict[str, object]]:
    """Create an auditable packet for human identity calibration.

    It intentionally contains no synthetic human judgments. Reviewers annotate `label`.
    """
    rows = []
    for i, m in enumerate(frontier_report.get("mechanisms", [])):
        if m.get("before_cluster") is None or m.get("after_cluster") is None:
            continue
        rows.append({
            "pair_id": f"match-{i:05d}",
            "stable_id": m.get("stable_id"),
            "before_cluster": m.get("before_cluster"),
            "after_cluster": m.get("after_cluster"),
            "model_similarity": m.get("similarity"),
            "model_margin": m.get("match_margin"),
            "model_ambiguous": bool(float(m.get("match_margin", 0.0)) < 0.05),
            "family": m.get("family"),
            "failure_type": m.get("failure_type"),
            "label": None,
            "notes": "",
        })
    return rows


def write_annotation_packet(path: str | Path, packet: Sequence[Mapping[str, object]]) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for row in packet:
            f.write(json.dumps(dict(row), sort_keys=True) + "\n")


def _labels(rows: Iterable[Mapping[str, object]]) -> Dict[str, str]:
    out = {}
    for r in rows:
        label = r.get("label")
        if label in LABELS:
            out[str(r["pair_id"])] = str(label)
    return out


def cohen_kappa(rows_a: Iterable[Mapping[str, object]], rows_b: Iterable[Mapping[str, object]]) -> Dict[str, object]:
    a = _labels(rows_a); b = _labels(rows_b); ids = sorted(set(a) & set(b))
    if not ids:
        return {"n": 0, "agreement": None, "kappa": None}
    agree = sum(a[i] == b[i] for i in ids) / len(ids)
    pa = {l: sum(a[i] == l for i in ids) / len(ids) for l in LABELS}
    pb = {l: sum(b[i] == l for i in ids) / len(ids) for l in LABELS}
    pe = sum(pa[l] * pb[l] for l in LABELS)
    kappa = (agree - pe) / (1 - pe) if pe < 1 else (1.0 if agree == 1 else 0.0)
    return {"n": len(ids), "agreement": float(agree), "kappa": float(kappa)}


def calibrate_matcher(packet: Iterable[Mapping[str, object]]) -> Dict[str, object]:
    """Score automatic same/different decisions against completed human labels."""
    rows = [r for r in packet if r.get("label") in ("same", "different")]
    if not rows:
        return {"n": 0, "accuracy": None, "precision_same": None, "recall_same": None}
    tp = fp = tn = fn = 0
    for r in rows:
        pred_same = not bool(r.get("model_ambiguous", False))
        true_same = r["label"] == "same"
        if pred_same and true_same: tp += 1
        elif pred_same and not true_same: fp += 1
        elif not pred_same and not true_same: tn += 1
        else: fn += 1
    n = len(rows)
    return {
        "n": n,
        "accuracy": float((tp + tn) / n),
        "precision_same": float(tp / max(1, tp + fp)),
        "recall_same": float(tp / max(1, tp + fn)),
        "confusion": {"tp": tp, "fp": fp, "tn": tn, "fn": fn},
    }
