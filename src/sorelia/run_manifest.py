from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
import hashlib
import json
import os
import platform
import sys
import time


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def source_tree_digest(root: str | Path) -> str:
    root = Path(root)
    h = hashlib.sha256()
    files = sorted(p for p in root.rglob('*.py') if '.pytest_cache' not in p.parts and '__pycache__' not in p.parts)
    for p in files:
        h.update(str(p.relative_to(root)).encode())
        h.update(b'\0')
        h.update(p.read_bytes())
        h.update(b'\0')
    return h.hexdigest()


def build_run_manifest(config_path: str | Path, mode: str, extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
    config_path = Path(config_path)
    repo_root = Path(__file__).resolve().parents[2]
    manifest: Dict[str, Any] = {
        'schema_version': 1,
        'mode': mode,
        'created_unix': int(time.time()),
        'python': sys.version.split()[0],
        'platform': platform.platform(),
        'executable': sys.executable,
        'config_path': str(config_path),
        'config_sha256': sha256_file(config_path),
        'source_tree_sha256': source_tree_digest(repo_root / 'src'),
        'pid': os.getpid(),
    }
    if extra:
        manifest['experiment'] = extra
    return manifest


def write_run_manifest(path: str | Path, manifest: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding='utf-8')
