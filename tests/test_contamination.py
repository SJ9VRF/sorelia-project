from sorelia.analysis.contamination import contamination_report, assert_no_exact_leakage
from sorelia.benchmarks.tasks import make_tasks


def test_contamination_detects_exact_overlap_and_clean_split():
    a = make_tasks(5, seed=1, prefix='a')
    b = make_tasks(5, seed=2, prefix='b')
    clean = contamination_report(a, b)
    assert clean['passes_exact_leakage_gate']
    dirty = contamination_report(a, [a[0], *b])
    assert not dirty['passes_exact_leakage_gate']
    assert dirty['exact_semantic_overlap_count'] >= 1


def test_assert_no_exact_leakage_returns_report():
    a = make_tasks(3, seed=10, prefix='train')
    b = make_tasks(3, seed=11, prefix='eval')
    r = assert_no_exact_leakage(a, b)
    assert r['task_id_overlap_count'] == 0
