from pathlib import Path
import yaml
from sorelia.experiments_ablation import run_ablations


def test_negative_controls_execute_and_preserve_leakage_gate(tmp_path):
    cfg = {
        'seed': 3,
        'benchmark': {'train_tasks': 18, 'eval_tasks': 12, 'stress_eval_tasks': 6, 'eval_trials': 1},
        'sorelia': {'iterations': 1},
        'clustering': {'k': 4},
        'generation': {'budget': 12},
        'curriculum': {'exploration_ratio': 0.2},
    }
    cp=tmp_path/'c.yaml'; cp.write_text(yaml.safe_dump(cfg))
    r=run_ablations(str(cp), str(tmp_path/'a.json'))
    assert 'shuffled_failure_labels' in r['summary']
    assert 'random_cluster_assignment' in r['summary']
    assert r['summary']['shuffled_failure_labels']['exact_eval_leakage'] == 0
    assert r['summary']['random_cluster_assignment']['exact_eval_leakage'] == 0
