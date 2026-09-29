from sorelia.benchmarks.tasks import make_tasks
from sorelia.agents.policy import PolicyAgent
from sorelia.infra.rollout import run_suite
from sorelia.clustering.failures import extract_failure_points, cluster, summarize

def test_failure_clustering():
    tr = run_suite(PolicyAgent(seed=2), make_tasks(24, seed=2))
    pts = extract_failure_points(tr)
    if pts:
        labels, meta = cluster(pts, k=5, seed=2)
        s = summarize(pts, labels)
        assert len(labels) == len(pts)
        assert meta["k"] <= len(pts)
        assert sum(x["size"] for x in s.values()) == len(pts)
