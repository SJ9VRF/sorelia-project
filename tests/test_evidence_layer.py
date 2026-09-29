from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def test_evidence_layer_public_contract():
    required=[
        'docs/EXPERIMENT_JOURNAL.md','docs/FAILED_EXPERIMENTS.md','docs/UNEXPECTED_FINDINGS.md',
        'docs/DECISION_LOG.md','docs/RAW_ARTIFACT_INDEX.md','website/evidence.html',
        'artifacts/eval_runs/browser_smoke.json','artifacts/failure_examples/browser-real-0001.json',
        'artifacts/ablations/v100_ablations.json','artifacts/plots/v080_curriculum_success.png',
        'artifacts/plots/v110_risk_displacement.png'
    ]
    for rel in required:
        p=ROOT/rel
        assert p.exists(), rel
        assert p.stat().st_size>100, rel

def test_homepage_exposes_research_process_layer():
    page=(ROOT/'website/index.html').read_text()
    assert 'Inside the research process' in page
    assert '9' in page and 'journaled experiments' in page
    assert '6' in page and 'failed assumptions' in page
    assert '8' in page and 'major decisions' in page
    assert 'evidence.html' in page
    assert 'FAILED_EXPERIMENTS.md' in page
    assert 'REVIEWER_REPRODUCTION.md' in page

def test_experiment_logs_have_required_fields():
    logs=sorted((ROOT/'artifacts/experiment_logs').glob('exp-*.md'))
    assert len(logs)==9
    for p in logs:
        t=p.read_text()
        for h in ['## Hypothesis','## Setup','## Result','## Interpretation','## Next decision']:
            assert h in t, (p.name,h)

def test_failed_experiments_are_evidence_grounded():
    t=(ROOT/'docs/FAILED_EXPERIMENTS.md').read_text()
    assert 'v0.5 comparison' in t
    assert 'Synthetic token/cost accounting' in t
    assert 'SORELIA superiority claim' in t

def test_raw_failure_example_matches_retained_browser_artifact():
    raw=json.load(open(ROOT/'artifacts/failure_examples/browser-real-0001.json'))
    full=json.load(open(ROOT/'artifacts/browser_smoke.json'))['trajectories'][0]
    assert raw['trajectory_id']==full['trajectory_id']
    assert raw['failure_events']==full['failure_events']


def test_evidence_page_local_links_exist():
    import re
    page=ROOT/'website/evidence.html'
    text=page.read_text()
    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith(('#','http://','https://','mailto:')):
            continue
        assert (page.parent/href).resolve().exists(), href
