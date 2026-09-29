from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List
import json

FORBIDDEN_PUBLIC_CLAIMS = (
    'outperforms state-of-the-art',
    'outperforms sota',
    'state-of-the-art performance',
    'best-performing',
)


def audit_repository(root: str | Path) -> Dict[str, Any]:
    root = Path(root)
    reg_path = root / 'docs' / 'CLAIM_EVIDENCE_REGISTRY.json'
    errors: List[str] = []
    warnings: List[str] = []
    if not reg_path.exists():
        return {'ok': False, 'errors': ['missing claim evidence registry'], 'warnings': []}
    registry = json.loads(reg_path.read_text(encoding='utf-8'))
    for c in registry.get('claims', []):
        cid = c.get('id', '?')
        status = c.get('status')
        evidence = c.get('evidence', [])
        if status == 'supported' and not evidence:
            errors.append(f'{cid}: supported claim has no evidence')
        for rel in evidence:
            if not (root / rel).exists():
                errors.append(f'{cid}: missing evidence file: {rel}')

    # Public-facing prose may describe unsupported claims only in explicit negative/audit contexts.
    for rel in ['README.md', 'website/index.html']:
        p = root / rel
        if not p.exists():
            errors.append(f'missing public artifact: {rel}')
            continue
        text = p.read_text(encoding='utf-8').lower()
        for phrase in FORBIDDEN_PUBLIC_CLAIMS:
            if phrase in text:
                errors.append(f'{rel}: forbidden unsupported public claim phrase: {phrase}')


    # Version consistency across package and public surfaces.
    try:
        import re
        py = (root / 'pyproject.toml').read_text(encoding='utf-8')
        m = re.search(r'^version\s*=\s*"([^"]+)"', py, flags=re.M)
        version = m.group(1) if m else None
        if not version:
            errors.append('pyproject.toml: missing project version')
        else:
            for rel in ['README.md', 'website/index.html', 'docs/RELEASE_STATUS.md']:
                p = root / rel
                if p.exists() and version not in p.read_text(encoding='utf-8'):
                    errors.append(f'{rel}: public version does not match pyproject {version}')
    except Exception as exc:
        errors.append(f'version consistency audit failed: {exc}')

    manifest = root / 'MANIFEST.sha256'
    if not manifest.exists():
        warnings.append('release checksum manifest missing')
    return {'ok': not errors, 'errors': errors, 'warnings': warnings, 'claims': len(registry.get('claims', []))}
