from sorelia.generation.generator import generate_from_clusters
from sorelia.generation.verify import filter_verified

def test_generated_tasks_have_lineage():
    summary = {0: {'size': 2, 'failure_type': 'grounding', 'family': 'browser', 'severity': .5, 'recoverability': .8, 'difficulty': .5, 'failure_ids': ['f1','f2']}}
    tasks = generate_from_clusters(summary, {0: 3}, iteration=2, seed=1)
    kept, rejected = filter_verified(tasks)
    assert len(kept) + len(rejected) == 3
    assert all(t.source_cluster == 0 for t in tasks)
    assert all(t.generation_iteration == 2 for t in tasks)
    assert all(t.generator_version for t in tasks)
    assert all(t.mutation_signature for t in tasks)
