from sorelia.benchmarks.tasks import make_tasks
from sorelia.generation.verify import verify_task

def test_generated_base_tasks_are_solvable():
    for t in make_tasks(20, seed=3):
        ok, reason = verify_task(t)
        assert ok, reason
