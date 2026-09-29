from pathlib import Path
from sorelia.pipeline import run_experiment

def test_end_to_end(tmp_path):
    cfg = Path(__file__).parents[1] / "configs" / "smoke.yaml"
    result = run_experiment(str(cfg), str(tmp_path / "run"))
    assert len(result["history"]) == 4
    assert (tmp_path / "run" / "metrics.json").exists()
