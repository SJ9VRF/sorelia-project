from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_public_repository_governance_files_exist():
    required = [
        'CONTRIBUTING.md', 'SECURITY.md', 'CODE_OF_CONDUCT.md',
        'docs/BENCHMARK_CARD.md', 'docs/SYSTEM_CARD.md',
        'docs/EXPERIMENT_REGISTRY.md', 'docs/DECISION_LOG.md',
        'docs/REVIEWER_REPRODUCTION.md', 'scripts/reviewer_demo.sh',
        '.github/PULL_REQUEST_TEMPLATE.md',
        '.github/ISSUE_TEMPLATE/bug.yml', '.github/ISSUE_TEMPLATE/research.yml',
    ]
    missing = [p for p in required if not (ROOT / p).exists()]
    assert not missing, f'missing public-repo artifacts: {missing}'


def test_experiment_registry_separates_executed_and_pending():
    text = (ROOT / 'docs/EXPERIMENT_REGISTRY.md').read_text()
    assert 'Executed' in text
    assert 'Pending' in text
    assert 'real trainable vlm post-training' in text.lower()
    assert 'must not be cited as completed evidence' in text


def test_reviewer_demo_preserves_truth_boundary():
    text = (ROOT / 'scripts/reviewer_demo.sh').read_text()
    assert 'sorelia.cli audit' in text
    assert 'run_browser_smoke.py' in text
    assert 'Not claimed:' in text
    assert 'SOTA' in text


def test_release_tree_has_no_python_cache_directories():
    tracked = [ROOT / '.pytest_cache']
    assert not any(p.exists() for p in tracked), 'pytest cache should not be present in a clean release snapshot'
