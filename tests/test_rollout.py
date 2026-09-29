from sorelia.benchmarks.tasks import make_tasks
from sorelia.agents.policy import PolicyAgent
from sorelia.infra.rollout import run_suite
from sorelia.evals.metrics import compute_metrics

def test_rollout_has_trace_and_metrics():
    agent = PolicyAgent(seed=1)
    ts = make_tasks(8, seed=1)
    trajs = run_suite(agent, ts)
    assert len(trajs) == 8
    assert all(t.num_steps > 0 for t in trajs)
    m = compute_metrics(trajs)
    assert 0 <= m["task_success_rate"] <= 1
    assert m["failure_events"] >= 0
