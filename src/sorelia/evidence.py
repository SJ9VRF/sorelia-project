from __future__ import annotations
from pathlib import Path
from typing import Dict, Iterable, List, Any
import hashlib
import json


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def build_evidence_index(root: str | Path, patterns: Iterable[str] = ('*.json', '*.jsonl', '*.txt')) -> List[Dict[str, Any]]:
    root = Path(root)
    files = []
    seen = set()
    for pattern in patterns:
        for p in sorted(root.rglob(pattern)):
            if not p.is_file() or p.name == 'evidence_index.json':
                continue
            rp = str(p.relative_to(root))
            if rp in seen:
                continue
            seen.add(rp)
            files.append({'path': rp, 'bytes': p.stat().st_size, 'sha256': _sha(p)})
    return files


def write_evidence_index(root: str | Path) -> Dict[str, Any]:
    root = Path(root)
    payload = {'schema_version': 1, 'files': build_evidence_index(root)}
    (root / 'evidence_index.json').write_text(json.dumps(payload, indent=2, sort_keys=True), encoding='utf-8')
    return payload
