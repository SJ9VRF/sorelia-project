from sorelia.benchmarks.tasks import make_tasks
from sorelia.agents.policy import PolicyAgent
from sorelia.infra.rollout import run_suite_repeated

def test_repeated_trials_have_unique_cells():
    tasks = make_tasks(4, seed=1, prefix="t")
    out = run_suite_repeated(PolicyAgent(seed=1), tasks, trials=3)
    assert len(out) == 12
    assert len({x.task_id for x in out}) == 12
    assert len({x.seed for x in out}) >= 3
