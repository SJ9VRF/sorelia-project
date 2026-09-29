from pathlib import Path
import yaml
from sorelia.experiments_ablation import run_ablations


def test_core_ablation_harness(tmp_path: Path):
    cfg={
      'seed':0,
      'benchmark':{'train_tasks':8,'eval_tasks':8,'stress_eval_tasks':4,'eval_trials':1},
      'sorelia':{'iterations':2},'clustering':{'k':3},'generation':{'budget':8},
      'curriculum':{'exploration_ratio':.2},'rollout':{'allow_recovery':True}}
    cp=tmp_path/'c.yaml'; cp.write_text(yaml.safe_dump(cfg))
    r=run_ablations(str(cp), str(tmp_path/'a.json'))
    expected = {
        'full','static_priority','no_exploration','single_iteration',
        'shuffled_failure_labels','random_cluster_assignment'
    }
    assert set(r['summary']) == expected
    assert r['summary']['full']['iterations'] == 2
    assert r['summary']['single_iteration']['iterations'] == 1
    assert r['summary']['no_exploration']['exploration_ratio'] == 0.0
    assert r['summary']['shuffled_failure_labels']['experimental_control'] == 'shuffled_failure_labels'
    assert r['summary']['random_cluster_assignment']['experimental_control'] == 'random_cluster_assignment'
