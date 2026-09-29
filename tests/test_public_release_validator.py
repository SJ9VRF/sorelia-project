from pathlib import Path
import subprocess, sys

def test_public_release_validator_passes():
    root=Path(__file__).resolve().parents[1]
    p=subprocess.run([sys.executable, str(root/'scripts/validate_public_release.py')], cwd=root, capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
