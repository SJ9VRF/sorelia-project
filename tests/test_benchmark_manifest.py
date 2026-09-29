from sorelia.benchmark_manifest import build_benchmark_manifest
from sorelia.benchmarks.tasks import make_tasks


def test_benchmark_manifest_is_deterministic_and_split_specific():
    train = make_tasks(4, seed=1, prefix="train")
    ev = make_tasks(3, seed=2, prefix="eval")
    a = build_benchmark_manifest(train, ev)
    b = build_benchmark_manifest(train, ev)
    assert a == b
    assert a["splits"]["train"]["sha256"] != a["splits"]["eval"]["sha256"]
    assert a["splits"]["eval"]["count"] == 3
