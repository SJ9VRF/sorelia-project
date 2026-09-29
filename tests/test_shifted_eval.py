from sorelia.benchmarks.tasks import make_tasks, make_shifted_tasks

def test_shifted_tasks_are_harder_and_longer():
    base = make_tasks(40, seed=7)
    stress = make_shifted_tasks(40, seed=7)
    assert sum(t.difficulty for t in stress)/len(stress) > sum(t.difficulty for t in base)/len(base)
    assert sum(t.horizon for t in stress)/len(stress) > sum(t.horizon for t in base)/len(base)
    assert all(t.task_id.startswith('stress-') for t in stress)
