from pathlib import Path
import hashlib, json, sys
root=Path(__file__).resolve().parents[1]
ledger=json.loads((root/'docs/EVIDENCE_LEDGER.json').read_text())
errors=[]
for t in ledger['threads']:
    if not t.get('experiments') or not t.get('decisions') or not t.get('current_conclusion'):
        errors.append(f"{t['id']}: incomplete thread metadata")
    if not t.get('implementation'):
        errors.append(f"{t['id']}: no implementation links")
    for field in ('evidence','implementation'):
        for e in t.get(field,[]):
            p=root/e['path']
            if not p.exists():
                errors.append(f"{t['id']}: missing {field} {e['path']}")
                continue
            h=hashlib.sha256(p.read_bytes()).hexdigest()
            if h!=e['sha256']:
                errors.append(f"{t['id']}: {field} hash mismatch {e['path']}")
for doc in ['docs/TRACEABILITY_MATRIX.md','docs/RESEARCH_THREADS.md','website/traceability.html']:
    if not (root/doc).exists(): errors.append(f'missing {doc}')
print(json.dumps({'ok':not errors,'threads':len(ledger['threads']),'errors':errors},indent=2))
sys.exit(1 if errors else 0)
