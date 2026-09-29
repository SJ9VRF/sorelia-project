import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_evidence_ledger_paths_and_hashes():
    ledger=json.loads((ROOT/'docs/EVIDENCE_LEDGER.json').read_text())
    assert ledger['release']=='1.7.0'
    assert len(ledger['threads'])>=4
    for t in ledger['threads']:
        assert t['experiments'] and t['decisions'] and t['current_conclusion']
        assert t['evidence']
        for e in t['evidence']:
            p=ROOT/e['path']; assert p.exists(), e['path']
            assert hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256']
def test_traceability_docs_expose_history_boundary():
    text=(ROOT/'docs/TRACEABILITY_MATRIX.md').read_text()
    assert 'retained Git history' in text
    assert 'does not reconstruct' in text
    assert 'THREAD-001' in text and 'THREAD-004' in text

def test_evidence_ledger_links_implementation_and_config():
    ledger=json.loads((ROOT/'docs/EVIDENCE_LEDGER.json').read_text())
    for t in ledger['threads']:
        assert t['implementation']
        for e in t['implementation']:
            p=ROOT/e['path']; assert p.exists(), e['path']
            assert hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256']
