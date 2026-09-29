from pathlib import Path
from sorelia.audit import audit_repository


def test_claim_evidence_release_audit_passes():
    root = Path(__file__).parents[1]
    result = audit_repository(root)
    assert result['ok'], result['errors']
