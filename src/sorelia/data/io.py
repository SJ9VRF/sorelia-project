from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable
from dataclasses import asdict


def write_jsonl(path, rows: Iterable):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            if hasattr(r, "to_dict"):
                r = r.to_dict()
            elif hasattr(r, "__dataclass_fields__"):
                r = asdict(r)
            f.write(json.dumps(r, sort_keys=True) + "\n")


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)
