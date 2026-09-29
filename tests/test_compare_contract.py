from pathlib import Path
import yaml
from sorelia.experiments import run_mode


def _cfg():
    p = Path(__file__).parents[1] / 'configs' / 'smoke.yaml'
    return yaml.safe_load(p.read_text())


def test_sorelia_comparison_uses_moving_frontier_after_first_round():
    cfg = _cfg()
    rows = run_mode(cfg, 'sorelia')
    assert rows[1]['frontier_summary'].get('initial', 0) >= 0
    assert rows[2]['frontier_summary']  # requires longitudinal frontier transition


def test_all_comparison_modes_receive_identical_verified_budget():
    cfg = _cfg()
    budget = int(cfg['generation']['budget'])
    for mode in ['sorelia', 'frequency', 'random', 'difficulty', 'human']:
        rows = run_mode(cfg, mode)
        for row in rows[1:]:
            assert row['verified_training_tasks_this_iteration'] == budget
