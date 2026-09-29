from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
from typing import Iterable
import hashlib, json
from .schema import Task


def _task_fingerprint(task: Task) -> str:
    stable = asdict(task).copy()
    # Provenance fields can differ for generated tasks; benchmark split identity should not.
    for key in ["source_failure_id", "source_cluster", "generation_iteration", "generator_version", "verifier_version"]:
        stable.pop(key, None)
    raw = json.dumps(stable, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def build_benchmark_manifest(train: Iterable[Task], eval_: Iterable[Task], stress: Iterable[Task] = ()) -> dict:
    train, eval_, stress = list(train), list(eval_), list(stress)
    splits = {}
    for name, tasks in [("train", train), ("eval", eval_), ("stress", stress)]:
        rows = [{"task_id": t.task_id, "family": t.family, "failure_mode": t.failure_mode,
                 "seed": t.seed, "fingerprint": _task_fingerprint(t)} for t in tasks]
        digest = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()
        splits[name] = {"count": len(rows), "sha256": digest, "tasks": rows}
    return {"schema_version": 1, "splits": splits}


def write_benchmark_manifest(path: str | Path, manifest: dict) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
